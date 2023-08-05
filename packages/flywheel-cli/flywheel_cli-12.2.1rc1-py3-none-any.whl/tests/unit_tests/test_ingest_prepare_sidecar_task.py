from unittest import mock

import pytest

from flywheel_cli.ingest import config
from flywheel_cli.ingest import schemas as T
from flywheel_cli.ingest.tasks.prepare_sidecar import PrepareSidecarTask


@pytest.fixture(scope="function")
def prepare_sidecar_task(db):
    ingest = db.create_ingest(status="preparing_sidecar")
    task = db.create_task(type="prepare_sidecar", ingest_id=ingest.id)

    prep_task = PrepareSidecarTask(
        db=db.client, task=task.schema(), worker_config=config.WorkerConfig()
    )

    return prep_task


def test_create_sidecar_containers(prepare_sidecar_task, db, mocker):
    mocker.patch(
        "flywheel_cli.ingest.tasks.prepare_sidecar.time.time", return_value=12345
    )
    con1 = db.create_container(
        path="group", level="group", src_context={"src": "src1", "label": "label1"},
    )
    con2 = db.create_container(
        path="group/project",
        level="project",
        src_context={"src": "src2", "label": "project"},
        parent_id=con1.id,
    )
    con3 = db.create_container(
        path="group/project/subject", level="subject", src_context={}, parent_id=con2.id
    )

    item1 = db.create_item(filename="a.txt", container_id=con2.id, skipped=True)
    item2 = db.create_item(filename="b.txt", container_id=con3.id, skipped=True)
    item3 = db.create_item(filename="c.txt", container_id=con3.id)

    prepare_sidecar_task._create_sidecar_containers()
    prepare_sidecar_task.update_items.flush()

    item = db.client.get_item(item3.id)
    assert item.container_id == con3.id

    sidecar_containers = {}
    containers = list(db.client.get_all_container())
    assert len(containers) == 5

    for container in containers:
        if container.level == T.ContainerLevel.group:
            sidecar_containers[container.level] = container
            continue

        if not container.sidecar:
            continue

        sidecar_containers[container.level] = container

    # group
    assert sidecar_containers[T.ContainerLevel.group].id == con1.id

    # project
    assert sidecar_containers[T.ContainerLevel.project].id != con2.id
    assert sidecar_containers[T.ContainerLevel.project].path == "group/project_12345"
    assert sidecar_containers[T.ContainerLevel.project].parent_id == con1.id
    assert sidecar_containers[T.ContainerLevel.project].src_context == {
        "src": "src2",
        "label": "project_12345",
    }

    # subject
    assert sidecar_containers[T.ContainerLevel.subject].id != con3.id
    assert (
        sidecar_containers[T.ContainerLevel.subject].path
        == "group/project_12345/subject"
    )
    assert (
        sidecar_containers[T.ContainerLevel.subject].parent_id
        == sidecar_containers[T.ContainerLevel.project].id
    )

    item = db.client.get_item(item1.id)
    assert item.container_id == sidecar_containers[T.ContainerLevel.project].id

    item = db.client.get_item(item2.id)
    assert item.container_id == sidecar_containers[T.ContainerLevel.subject].id

    assert prepare_sidecar_task.sidecar_project_name == "project_12345"
    assert prepare_sidecar_task.original_project_name == "project"
    assert prepare_sidecar_task.original_project.id == con2.id


def test_run(prepare_sidecar_task, db, mocker, sdk_mock):
    missing_perm_mock = mock.Mock(access="ro", id="user@user.io")

    def get_project_side_effect(project_id, *_, **__):
        if project_id == "original_pid":
            return mock.Mock(
                permissions=[
                    mock.Mock(access="admin", id="dev@flywheel.io"),
                    missing_perm_mock,
                ]
            )
        return mock.Mock(permissions=[mock.Mock(access="admin", id="dev@flywheel.io"),])

    sdk_mock.add_project.return_value = "pid"
    sdk_mock.add_subject.return_value = "sub_id"
    sdk_mock.get_project.side_effect = get_project_side_effect
    sdk_mock.api_client.call_api.return_value = [
        {
            "all": [],
            "project_id": "5ef453dbddcc77001d20cb2d",
            "name": "name",
            "auto_update": True,
            "disabled": False,
            "gear_id": "5ef4537addcc77001720cb2e",
            "not": [],
            "_id": "5ef453f6ddcc77001920cb2d",
            "any": [{"type": "file.modality", "value": "mod"}],
        }
    ]
    mocker.patch(
        "flywheel_cli.ingest.tasks.prepare_sidecar.time.time", return_value=12345
    )

    con1 = db.create_container(
        path="group",
        level="group",
        src_context={"src": "src1", "label": "label1"},
        dst_context={"_id": "12345", "src": "src1", "label": "label1"},
    )
    con2 = db.create_container(
        path="group/project",
        level="project",
        src_context={"src": "src2", "label": "project"},
        parent_id=con1.id,
        dst_context={"_id": "original_pid"},
    )
    con3 = db.create_container(
        path="group/project/subject",
        level="subject",
        src_context={"src": "src3", "label": "label3"},
        parent_id=con2.id,
    )

    item1 = db.create_item(filename="a.txt", container_id=con2.id, skipped=True)
    item2 = db.create_item(filename="b.txt", container_id=con3.id, skipped=True)
    item3 = db.create_item(filename="c.txt", container_id=con3.id)

    prepare_sidecar_task._run()

    tasks = list(db.client.get_all_task())
    assert len(tasks) == 3
    for task in tasks:
        if task.id == prepare_sidecar_task.task.id:
            continue
        assert task.type == T.TaskType.upload
        assert task.item_id in [item1.id, item2.id]

    assert sdk_mock.mock_calls == [
        mock.call.add_project(
            {"src": "src2", "label": "project_12345", "group": "12345"}
        ),
        mock.call.get_project("original_pid"),
        mock.call.get_project("pid"),
        mock.call.add_project_permission("pid", missing_perm_mock),
        mock.call.api_client.call_api(
            "/projects/original_pid/rules",
            "GET",
            _return_http_data_only=True,
            auth_settings=["ApiKey"],
            response_type=object,
        ),
        mock.call.api_client.call_api(
            "/projects/pid/rules",
            "GET",
            _return_http_data_only=True,
            auth_settings=["ApiKey"],
            response_type=object,
        ),
        mock.call.remove_project_rule("pid", "5ef453f6ddcc77001920cb2d"),
        mock.call.add_project_rule(
            "pid",
            {
                "all": [],
                "project_id": "pid",
                "name": "name",
                "auto_update": True,
                "disabled": False,
                "gear_id": "5ef4537addcc77001720cb2e",
                "not": [],
                "any": [{"type": "file.modality", "value": "mod"}],
            },
        ),
        mock.call.add_subject(
            {"src": "src3", "label": "label3", "project": "pid", "code": "label3"}
        ),
    ]

    ingest = db.client.ingest
    assert ingest.status == T.IngestStatus.uploading
