import pytest

from flywheel_cli.ingest import errors
from flywheel_cli.ingest import schemas as T
from flywheel_cli.ingest.scanners import filename
from .conftest import DummyWalker


def test_validate_opts():
    with pytest.raises(ValueError):
        filename.FilenameScanner.validate_opts(None)

    with pytest.raises(ValueError):
        filename.FilenameScanner.validate_opts({"key": "value"})

    with pytest.raises(ValueError):
        filename.FilenameScanner.validate_opts({"pattern": None})
    filename.FilenameScanner.validate_opts({"pattern": "{group}-{project._id}"})


def test_scan():
    walker = DummyWalker(
        ["path/group_project_session_subject-acquisition.txt", "dir1/dir2/file2"]
    )

    scanner = filename.FilenameScanner(
        ingest_config=None,
        strategy_config=None,
        worker_config=None,
        walker=walker,
        opts={"pattern": "{group}_{project}_{session}_{subject}-{acquisition}.txt"},
        context={},
    )

    scan_results = list(scanner.scan("dir"))
    assert len(scan_results) == 2

    # match
    item = scan_results[0]
    assert isinstance(item, T.Item)
    assert item.type == "file"
    assert item.dir == "dir/path"
    assert item.files == ["group_project_session_subject-acquisition.txt"]
    assert item.files_cnt == 1
    assert item.bytes_sum == 1
    assert item.context.dict(exclude_none=True) == {
        "group": {"id": "group"},
        "project": {"label": "project"},
        "session": {"label": "session"},
        "subject": {"label": "subject"},
        "acquisition": {"label": "acquisition"},
    }

    # not match
    error = scan_results[1]
    assert error.filepath == "dir1/dir2/file2"
    assert error.code == errors.FilenameDoesNotMatchTemplate.code
    assert error.message == (
        "File dir1/dir2/file2 did not match the template "
        "{group}_{project}_{session}_{subject}-{acquisition}.txt"
    )
