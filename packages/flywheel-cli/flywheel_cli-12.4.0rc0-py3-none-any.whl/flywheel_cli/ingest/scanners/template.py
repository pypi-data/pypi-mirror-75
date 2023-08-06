"""Provides TemplateScanner class"""

import copy
import logging
from collections import deque

import fs
from pydantic import ValidationError

from ... import util
from .. import errors
from .. import schemas as s
from ..strategies.factory import create_strategy
from ..template import TERMINAL_NODE
from .abstract import AbstractScanner

log = logging.getLogger(__name__)


class TemplateScanner(AbstractScanner):
    """Template scanner"""

    def _scan(self, subdir):
        import_strategy = create_strategy(self.strategy_config)
        import_strategy.initialize()
        initial_context = import_strategy.initial_context()
        root_node = import_strategy.root_node

        prev_dir = None
        prev_node = root_node
        prev_context = copy.deepcopy(initial_context)
        files = {}

        if root_node.node_type == "scanner":
            yield from self.create_task_or_item(subdir, root_node, initial_context, {})
            # stop when the root node is a scanner, like in case of dicom strategy
            return

        # TODO: determine according to the hierarcy how walk the input folder
        for fileinfo in self.iter_files(subdir):
            context = copy.deepcopy(initial_context)
            path_parts = deque(fileinfo.name.split("/"))
            node = root_node
            parent_dirpath = "/"
            while len(path_parts) > 1:
                dirname = path_parts.popleft()
                parent_dirpath = fs.path.combine(parent_dirpath, dirname)
                node = node.extract_metadata(
                    dirname, context, self.walker, path=parent_dirpath
                )
                if node in (None, TERMINAL_NODE):
                    break

            if prev_dir and prev_dir != parent_dirpath:
                yield from self.create_task_or_item(
                    prev_dir, prev_node, prev_context, files
                )
                files = {}

            rel_filepath = fs.path.join(*path_parts)
            files[rel_filepath] = fileinfo
            prev_dir = parent_dirpath
            prev_node = node
            prev_context = context

        yield from self.create_task_or_item(prev_dir, prev_node, prev_context, files)

    def create_task_or_item(self, dirpath, node, context, files):
        """Create ingest item or scan task according to the node type"""
        if node not in (None, TERMINAL_NODE) and node.node_type == "scanner":
            scan_context = copy.deepcopy(context)
            scan_context["scanner"] = {
                "type": node.scanner_type,
                "dir": dirpath,
                "opts": node.opts,
            }
            yield s.TaskIn(
                type=s.TaskType.scan, context=scan_context,
            )
            return

        # Merge subject and session if one of them is missing
        if self.strategy_config.no_subjects or self.strategy_config.no_sessions:
            self.context_merge_subject_and_session(context)

        if self.strategy_config.group_override:
            util.set_nested_attr(
                context, "group._id", self.strategy_config.group_override
            )

        if self.strategy_config.project_override:
            util.set_nested_attr(
                context, "project.label", self.strategy_config.project_override
            )

        try:
            # parse and validate item context
            item_context = s.ItemContext(**context)
        except ValidationError as exc:
            msg = f"Context is invalid for file. Details:\n{exc}"
            log.debug(msg)
            # add errors
            for filepath, fileinfo in files.items():
                self.file_errors.append(
                    s.Error(
                        code=errors.InvalidFileContext.code,
                        message=msg,
                        filepath=fileinfo.name,
                    )
                )
            return

        if item_context.packfile:
            packfile_size = sum(f.size for f in files.values())
            filename = item_context.packfile.name
            if not filename:
                parent_ctx = self._get_parent_context(item_context)
                cname = parent_ctx.label or parent_ctx.id
                packfile_type = item_context.packfile.type
                if not packfile_type or packfile_type == "zip":
                    filename = f"{cname}.zip"
                else:
                    filename = f"{cname}.{packfile_type}.zip"

            yield s.Item(
                type="packfile",
                dir=dirpath,
                filename=filename,
                files=list(files.keys()),
                files_cnt=len(files),
                bytes_sum=packfile_size,
                context=item_context,
            )
        else:
            for filepath, fileinfo in files.items():
                yield s.Item(
                    type="file",
                    dir=dirpath,
                    filename=fs.path.basename(filepath),
                    files=[filepath],
                    files_cnt=1,
                    bytes_sum=fileinfo.size,
                    context=item_context,
                )

    @staticmethod
    def _get_parent_context(context: s.ItemContext) -> s.SourceContainerContext:
        """
        Get parent container context from item context, like if group, project in the context
        this method will return the project context
        """
        for cont_level in ("acquisition", "session", "subject", "project", "group"):
            cont_ctx = getattr(context, cont_level, None)
            if cont_ctx:
                break
        return cont_ctx
