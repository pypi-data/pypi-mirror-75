from flywheel_cli.ingest import schemas as s


def test_ingest_status_is_terminal():
    # terminal ('finished', 'failed', 'aborted')
    assert s.IngestStatus.is_terminal("finished")
    assert s.IngestStatus.is_terminal("failed")
    assert s.IngestStatus.is_terminal("aborted")

    # not terminal
    assert not s.IngestStatus.is_terminal("created")
    assert not s.IngestStatus.is_terminal("scanning")
    assert not s.IngestStatus.is_terminal("resolving")
    assert not s.IngestStatus.is_terminal("in_review")
    assert not s.IngestStatus.is_terminal("preparing")
    assert not s.IngestStatus.is_terminal("uploading")
    assert not s.IngestStatus.is_terminal("finalizing")


def test_task_type_ingest_status():
    assert s.TaskType.ingest_status(s.TaskType.scan) == s.IngestStatus.scanning
    assert s.TaskType.ingest_status(s.TaskType.resolve) == s.IngestStatus.resolving
    assert s.TaskType.ingest_status(s.TaskType.prepare) == s.IngestStatus.preparing
    assert s.TaskType.ingest_status(s.TaskType.upload) == s.IngestStatus.uploading
    assert s.TaskType.ingest_status(s.TaskType.finalize) == s.IngestStatus.finalizing


def test_item_filename_label_sanitize():
    item = s.Item(
        type="file",
        dir="/",
        files=["file.txt"],
        filename="file/bar%\\2020-01-05 15:30.txt",
        context={
            "group": {"_id": "grp", "label": "grp/bar%\\2020-01-05 15:30"},
            "project": {"label": "prj/bar%\\2020-01-05 15:30"},
            "subject": {"label": "subj/bar%\\2020-01-05 15:30"},
            "session": {"label": "session/bar%\\2020-01-05 15:30"},
            "acquisition": {"label": "acq/bar%\\2020-01-05 15:30"},
        },
        files_cnt=1,
        bytes_sum=1,
    )
    assert item.context.group.label == "grp_bar%_2020-01-05 15_30"
    assert item.context.project.label == "prj_bar%_2020-01-05 15_30"
    assert item.context.subject.label == "subj_bar%_2020-01-05 15_30"
    assert item.context.session.label == "session_bar%_2020-01-05 15_30"
    assert item.context.acquisition.label == "acq_bar%_2020-01-05 15_30"
    assert item.filename == "file_bar%_2020-01-05 15_30.txt"
