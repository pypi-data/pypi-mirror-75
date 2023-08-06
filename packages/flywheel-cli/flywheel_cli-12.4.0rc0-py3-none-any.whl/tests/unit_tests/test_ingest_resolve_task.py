import datetime
from unittest import mock
from uuid import uuid4

import pytest
import flywheel

from flywheel_cli.ingest import config, errors
from flywheel_cli.ingest import models as M
from flywheel_cli.ingest import schemas as T
from flywheel_cli.ingest.tasks import resolve


@pytest.fixture(scope="function")
def resolve_task(sdk_mock):
    task = T.TaskOut(
        type="resolve",
        id=uuid4(),
        ingest_id=uuid4(),
        status="pending",
        timestamp=0,
        retries=0,
        history=[],
        created=datetime.datetime.now(),
    )
    resolve_task = resolve.ResolveTask(
        db=mock.Mock(**{"batch_writer_insert_container.return_value.batch_size": 999,}),
        task=task,
        worker_config=mock.Mock(),
    )
    resolve_task.ingest_config = config.IngestConfig(src_fs="/tmp",)

    return resolve_task


def test_fw_property(mocker, get_sdk_mock):
    db_client_mock = mock.Mock()
    db_client_mock.api_key = "api_key"

    resolve_task = resolve.ResolveTask(
        db=db_client_mock, task=mock.Mock(), worker_config=mock.Mock()
    )
    # make sure __init__ does not get the sdk
    get_sdk_mock.assert_not_called()

    fw = resolve_task.fw
    assert fw == get_sdk_mock.return_value

    get_sdk_mock.assert_called_once_with("api_key")


def test_on_success(resolve_task):
    resolve_task._on_success()

    resolve_task.db.set_ingest_status.assert_called_once_with(
        status=T.IngestStatus.in_review
    )
    resolve_task.db.review.assert_not_called()


def test_on_success_assume_yes(resolve_task):
    resolve_task.ingest_config.assume_yes = True

    resolve_task._on_success()

    resolve_task.db.set_ingest_status.assert_called_once_with(
        status=T.IngestStatus.in_review
    )
    resolve_task.db.review.assert_called_once()


def test_on_success_detect_duplicates(resolve_task):
    resolve_task.ingest_config.detect_duplicates = True

    resolve_task._on_success()

    resolve_task.db.start_detecting_duplicates.assert_called_once()


def test_on_error(resolve_task):
    resolve_task._on_error()
    resolve_task.db.fail.assert_called_once()
    resolve_task.db.set_ingest_status.assert_not_called()
    resolve_task.db.review.assert_not_called()


def test_resolve_item_containers(sdk_mock, resolve_task):
    sdk_mock.lookup.return_value.to_dict.return_value = {
        "id": "id2",
        "label": "label2",
        "files": [{"name": "name1"}, {"name": "name2"}],
    }
    item = T.Item(
        id=uuid4(),
        dir="dir",
        type="packfile",
        filename="test.zip",
        files=["file1", "file2"],
        files_cnt=2,
        bytes_sum=2,
        ingest_id=uuid4(),
        context={
            "group": {"_id": "gid"},
            "project": {"_id": "pid"},
            "session": {"_id": "sid"},
        },
    )

    container = resolve_task._resolve_item_containers(item)

    assert resolve_task.visited == {"gid", "gid/<id:pid>"}
    assert isinstance(container, T.Container)


def test_resolve_container_visited(resolve_task):
    resolve_task.visited.add("path")

    container = resolve_task._resolve_container(
        c_level=1,
        path=["path"],
        context={"_id": "idval", "label": "labelval"},
        parent=None,
    )

    assert container == resolve_task.db.find_one_container.return_value
    args, _ = resolve_task.db.find_one_container.call_args
    assert len(args) == 1
    condition = args[0]
    assert condition.compare(M.Container.path == "path")


def test_resolve_container_not_visited_no_parent(resolve_task, sdk_mock):
    sdk_mock.lookup.return_value.to_dict.return_value = {
        "id": "grp",
        "label": "grp",
    }
    resolve_task.insert_containers = mock.Mock()

    assert resolve_task.visited == set()

    ctx = T.SourceContainerContext(id="grp_id", label="grp_label")
    container = resolve_task._resolve_container(
        c_level=T.ContainerLevel(0), path=["grp"], context=ctx, parent=None
    )

    assert "grp" in resolve_task.visited
    assert isinstance(container, T.Container)
    assert container.path == "grp"
    assert container.level == 0
    assert container.src_context == ctx
    assert container.dst_context.dict(exclude_none=True) == {
        "id": "grp",
        "label": "grp",
        "files": [],
    }
    resolve_task.insert_containers.push.assert_called_once_with(container)


def test_resolve_container_not_visited_parent(resolve_task, sdk_mock):
    assert resolve_task.visited == set()

    src_ctx = T.SourceContainerContext(id="prj_id", label="prj")
    parent = T.Container(level=0, path="grp", src_context={"id": "grp"})
    container = resolve_task._resolve_container(
        c_level=T.ContainerLevel(1), path=["grp", "prj"], context=src_ctx, parent=parent
    )

    assert "grp/prj" in resolve_task.visited
    assert isinstance(container, T.Container)
    assert container.path == "grp/prj"
    assert container.level == 1
    assert container.src_context == src_ctx
    assert container.parent_id == parent.id
    # parent does not exist so child also does not exist
    assert container.dst_path is None
    assert container.dst_context is None
    # not call lookup if parent does not exist
    sdk_mock.lookup.assert_not_called()


def test__find_container_in_fw(resolve_task, sdk_mock):
    sdk_mock.lookup.return_value.to_dict.return_value = {
        "id": "bar_id",
        "label": "bar",
        "files": [{"name": "file1"}, {"name": "file2"}],
    }
    dst_context = resolve_task._find_container_in_fw(["foo", "bar"])
    assert dst_context.id == "bar_id"
    assert dst_context.label == "bar"
    assert dst_context.files == ["file1", "file2"]
    sdk_mock.lookup.assert_called_once_with(["foo", "bar"])


def test_run(resolve_task, sdk_mock):
    sdk_mock.lookup.return_value.to_dict.return_value = {
        "id": "bar_id",
        "label": "bar_label",
    }
    item_id = uuid4()
    resolve_task.db.count_all_item.return_value = 1
    resolve_task.db.get_all_item.return_value = [
        T.Item(
            id=item_id,
            dir="dir",
            type="packfile",
            filename="test.zip",
            files=["file1", "file2"],
            files_cnt=2,
            bytes_sum=2,
            ingest_id=uuid4(),
            context={
                "group": {"_id": "grp"},
                "project": {"label": "prj"},
                "packfile": {"type": "zip"},
            },
        )
    ]
    resolve_task.update_items = mock.Mock()
    resolve_task._run()

    resolve_task.update_items.push.assert_called_once_with(
        {"id": item_id, "container_id": mock.ANY, "existing": False,}
    )
    resolve_task.update_items.flush.assert_called_once()


def test_run_success(resolve_task):
    resolve_task.db.count_all_item.return_value = 0
    resolve_task.db.get_all_item.return_value = []

    resolve_task.run()

    resolve_task.db.update_task.assert_called_once_with(
        resolve_task.task.id, status=T.TaskStatus.completed
    )
    # success
    resolve_task.db.set_ingest_status.assert_called_once_with(
        status=T.IngestStatus.in_review
    )


def test_run_error(resolve_task):
    class FooException(Exception):
        pass

    resolve_task.db.get_all_item.side_effect = FooException()
    resolve_task.run()

    # not set ingest status directly
    resolve_task.db.set_ingest_status.assert_not_called()
    # resolve fails the whole ingest
    resolve_task.db.fail.assert_called_once()


def test_run_require_project(resolve_task, sdk_mock):
    resolve_task.ingest_config.require_project = True
    sdk_mock.lookup.side_effect = flywheel.ApiException()
    _id = uuid4()
    resolve_task.db.count_all_item.return_value = 1
    resolve_task.db.get_all_item.return_value = [
        T.Item(
            id=_id,
            dir="dir",
            type="file",
            filename="file",
            files=["file"],
            files_cnt=2,
            bytes_sum=2,
            ingest_id=uuid4(),
            context={"group": {"_id": "gid",}, "project": {"label": "prj"}},
        )
    ]
    resolve_task.update_items = mock.Mock()

    with pytest.raises(errors.ContainerDoesNotExist) as exc_info:
        resolve_task._run()

    assert (
        str(exc_info.value)
        == "The --require-project flag is set and group 'gid' does not exist"
    )
