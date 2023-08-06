"""Provides ResolveTask class."""

import logging
import typing as t
from uuid import UUID

import flywheel
import fs

from ... import errors as global_errors
from ... import util
from .. import errors as ingest_errors
from .. import models as m
from .. import schemas as s
from .abstract import Task

log = logging.getLogger(__name__)


class ResolveTask(Task):
    """Resolve containers for review"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.visited = set()
        self.insert_containers = self.db.batch_writer_insert_container()
        self.update_items = self.db.batch_writer_update_item(
            depends_on=self.insert_containers
        )
        self.update_uids = self.db.batch_writer_update_uid(
            depends_on=self.insert_containers
        )
        # cache size == number of container types (group, project, subject, session, acquisiton)
        self.cache = util.LRUCache(5)
        # insert containers cache that kept in sync with the batch writer
        self.insert_containers_cache = util.LRUCache(self.insert_containers.batch_size)
        self.uid_ids = None
        self.permission_errors = set()

    def _run(self):
        self.report_progress(total=self.db.count_all_item())

        for item in self.db.get_all_item():
            container = self._resolve_item_containers(item)
            if not container:
                log.warning(f"Couldn't resolve container for: {item.id}")
                continue

            dst_files = container.dst_context.files if container.dst_context else []
            update = {
                "id": item.id,
                "container_id": container.id,
                "existing": item.filename in dst_files,
            }

            self.update_items.push(update)

            # update progress
            self.report_progress(completed=1)

        # flush all remaining items to the db
        self.update_items.flush()
        self.update_uids.flush()

        if self.permission_errors:
            # TODO: maybe this can be removed once container and item errors are separated?
            # that would allow the user to skip projects with permission error, but
            # import everything else
            for err_msg in self.permission_errors:
                # add error expcept the last one
                self.db.add(
                    s.Error(
                        task_id=self.task.id,
                        code=ingest_errors.NotEnoughPermissions.code,
                        message=err_msg,
                    )
                )
            raise ingest_errors.StopIngestError()

        log.debug(f"Containers cache info: {self.cache}")
        log.debug(f"Insert containers cache info: {self.insert_containers_cache}")

    def _resolve_item_containers(self, item: s.Item) -> t.Optional[s.Container]:
        last = None
        path = []
        uid_updates = {}
        uid_ids = None

        def add_update(uids, container_type, container_id):
            for uid in uids:
                if not uid in uid_updates:
                    uid_updates[uid] = {"id": uid}
                uid_updates[uid][container_type] = container_id

        for c_level in s.ContainerLevel:
            cont_ctx = getattr(item.context, c_level.name, None)
            if not cont_ctx:
                break

            path.append(util.get_path_el(c_level.name, cont_ctx.dict(by_alias=True)))
            last = self._resolve_container(c_level, path, cont_ctx, last)

            if self.ingest_config.detect_duplicates:
                if not uid_ids:
                    # cache uid ids for the current item, otherwise it would be retrieved
                    # for
                    uid_ids = self._get_uid_ids_for_item(item)
                if last.level == s.ContainerLevel.session:
                    add_update(uid_ids, "session_container_id", last.id)

                if last.level == s.ContainerLevel.acquisition:
                    add_update(uid_ids, "acquisition_container_id", last.id)

        for update in uid_updates.values():
            self.update_uids.push(update)

        return last

    def _resolve_container(
        self,
        c_level: s.ContainerLevel,
        path: t.List[str],
        context: s.SourceContainerContext,
        parent: t.Optional[s.Container],
    ) -> s.Container:
        path_str = fs.path.join(*path)

        if path_str in self.visited:
            # already resolved container with this path
            return self._get_visited_container(path_str)

        self._check_container_permission(c_level, path)

        # create new container node
        child = s.Container(
            path=path_str,
            level=c_level,
            src_context=context,
            parent_id=parent.id if parent else None,
        )

        if not parent or parent.dst_path:
            # try to resolve if parent exists
            resolved = self._find_container_in_fw(path)

            if resolved:
                child.existing = True
                child.dst_context = resolved
                child.dst_path = util.get_path_el(
                    c_level.name, child.dst_context.dict(by_alias=True), use_labels=True
                )
                if parent and parent.dst_path:
                    child.dst_path = fs.path.join(parent.dst_path, child.dst_path)

        self._check_require_container(child)

        log.debug(f"Resolved {c_level.name} container: {path_str}")
        self.visited.add(path_str)
        self.insert_containers.push(child.dict())

        # store container in cache to make resolving faster
        self.cache[path_str] = child
        self.insert_containers_cache[path_str] = child
        return child

    def _check_container_permission(self, c_level, path):
        """
        Verify that the current user has enough permissions to create/upload into the
        given group/project
        """
        if c_level == s.ContainerLevel.group and self.ingest_config.copy_duplicates:
            try:
                self.fw.can_create_project_in_group(path[0])
            except global_errors.NotEnoughPermissions as exc:
                self.permission_errors.add(
                    "User does not have enough permissions to create sidecar project "
                    f"which is required for copy-duplicates. Reason: {exc}"
                )
        if c_level == s.ContainerLevel.project:
            try:
                self.fw.can_import_into(path[0], path[1])
            except global_errors.NotEnoughPermissions as exc:
                # instead of raising for the first error, collect all of them
                # so the user will have a better image about the permission errors
                self.permission_errors.add(str(exc))

    def _check_require_container(self, container):
        """If the require_project flag is set and the group/project does not exist raise ContainerDoesNotExist exception"""
        if (
            self.ingest_config.require_project
            and not container.existing
            and container.level in [s.ContainerLevel.group, s.ContainerLevel.project]
        ):
            container_label = container.src_context.label or container.src_context.id
            msg = f"{container.level.name} '{container_label}'"

            raise ingest_errors.ContainerDoesNotExist(
                f"The --require-project flag is set and {msg} does not exist"
            )

    def _find_container_in_fw(
        self, path: t.List[str]
    ) -> t.Optional[s.DestinationContainerContext]:
        """Attempt to find the container in FW"""
        try:
            container = self.fw.lookup(path).to_dict()
            files = container.pop("files", [])
            files = list(map(lambda f: f["name"], files))
            log.debug(f"Resolve: {path} - returned: {container['id']}")
            return s.DestinationContainerContext(**container, files=files)
        except flywheel.ApiException:
            log.debug(f"Resolve: {path} - NOT FOUND")
            return None

    def _get_visited_container(self, path: str) -> s.Container:
        """
        Get container that we already resolved either from cache or from database if we
        already wrote changes to the db
        """
        child = self.cache.get(path)
        if not child:
            # if not in cache try to get from insert cache
            child = self.insert_containers_cache.get(path)
        if not child:
            # if not in insert cache, it is already written to the db
            child = self.db.find_one_container(m.Container.path == path)
        # update cache, do not update insert_containers_cache here
        # because it will get out of sync from the insert containers batch writer
        self.cache[path] = child
        return child

    def _get_uid_ids_for_item(self, item: s.Item) -> t.Set[UUID]:
        """Get ids of UID rows for the given item"""
        uid_ids: t.Set[UUID] = set()
        for uid in self.db.get_all_uid(m.UID.item_id == item.id):
            uid_ids.add(uid.id)
        return uid_ids

    def _on_success(self):
        if self.ingest_config.detect_duplicates:
            self.db.start_detecting_duplicates()
        else:
            self.db.set_ingest_status(status=s.IngestStatus.in_review)
            if self.ingest_config.assume_yes:
                # ingest was started with assume yes so accept the review
                self.db.review()

    def _on_error(self):
        self.db.fail()
