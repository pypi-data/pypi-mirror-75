import datetime
import uuid
from unittest import mock

import pytest

from flywheel_cli.ingest import config
from flywheel_cli.ingest import schemas as T
from flywheel_cli.ingest.tasks import factory, finalize, prepare, resolve, scan, upload


@pytest.mark.parametrize(
    "task_type,init_kwargs,expected_task_cls",
    [
        ("scan", {"context": {"scanner": {"type": "template"}}}, scan.ScanTask),
        ("resolve", {}, resolve.ResolveTask),
        ("prepare", {}, prepare.PrepareTask),
        ("upload", {}, upload.UploadTask),
        ("finalize", {}, finalize.FinalizeTask),
    ],
)
def test_create_task(task_type, init_kwargs, expected_task_cls):
    task_out = T.TaskOut(
        id=uuid.uuid4(),
        type=task_type,
        created=datetime.datetime.now(),
        status="pending",
        timestamp=0,
        history=[("pending", 1)],
        ingest_id=uuid.uuid4(),
        retries=0,
        **init_kwargs,
    )
    db_client = mock.Mock()
    cfg = config.WorkerConfig()

    task = factory.create_task(client=db_client, task=task_out, worker_config=cfg)

    assert isinstance(task, expected_task_cls)
    assert task.db == db_client
    assert task.task == task_out
    assert task.worker_config == cfg
