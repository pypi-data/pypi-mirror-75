import pytest

from flywheel_cli.ingest import config
from flywheel_cli.ingest import errors
from flywheel_cli.ingest import schemas as s
from flywheel_cli.ingest.scanners import template

from .conftest import DummyWalker


def test_scan_with_folder_strategy():
    walker = DummyWalker(["group/project/subject/session/file", "random_file"])

    scanner = template.TemplateScanner(
        ingest_config=None,
        strategy_config=config.FolderConfig(),
        worker_config=None,
        walker=walker,
    )

    scan_results = list(scanner.scan("dir"))
    assert len(scan_results) == 2

    # match
    item = scan_results[0]
    assert isinstance(item, s.Item)
    assert item.type == "file"
    assert item.dir == "/group/project/subject/session"
    assert item.files == ["file"]
    assert item.files_cnt == 1
    assert item.bytes_sum == 1
    assert item.context.dict(exclude_none=True) == {
        "group": {"id": "group"},
        "project": {"label": "project"},
        "subject": {"label": "subject"},
        "session": {"label": "session"},
    }

    # not a match
    error = scan_results[1]
    assert isinstance(error, s.Error)
    assert error.filepath == "random_file"
    assert error.code == errors.InvalidFileContext.code
    assert error.message == (
        "Context is invalid for file. Details:\n"
        "2 validation errors for ItemContext\n"
        "group\n"
        "  field required (type=value_error.missing)\n"
        "project\n"
        "  field required (type=value_error.missing)"
    )


def test_scan_with_template_strategy():
    walker = DummyWalker(
        [
            "test_project1/subject1/session1/files/file.dcm",
            "test_project1/subject1/session1/files/file.txt",
            "subject1/file.dcm",
        ]
    )

    scanner = template.TemplateScanner(
        ingest_config=None,
        strategy_config=config.TemplateConfig(
            group="group_id",
            template=[
                {"pattern": "test_{project}"},
                {"pattern": "{subject}"},
                {"pattern": "{session}"},
                {"select": [{"pattern": ".*", "scan": "dicom"}]},
            ],
        ),
        worker_config=None,
        walker=walker,
    )

    scan_results = list(scanner.scan("dir"))

    assert len(scan_results) == 2

    # match, scan task
    task = scan_results[0]
    assert isinstance(task, s.TaskIn)
    assert task.type == "scan"
    assert task.context == {
        "group": {"_id": "group_id"},
        "project": {"label": "project1"},
        "subject": {"label": "subject1"},
        "session": {"label": "session1"},
        "scanner": {
            "type": "dicom",
            "dir": "/test_project1/subject1/session1/files",
            "opts": {},
        },
    }

    # not a match, error
    error = scan_results[1]
    assert isinstance(error, s.Error)
    assert error.filepath == "subject1/file.dcm"
    assert error.code == errors.InvalidFileContext.code
    assert error.message == (
        "Context is invalid for file. Details:\n"
        "1 validation error for ItemContext\n"
        "project\n"
        "  field required (type=value_error.missing)"
    )


@pytest.mark.parametrize(
    "packfile_opts,expected_packfile_name",
    [
        ({"packfile_type": "dicom"}, "session1.dicom.zip"),
        ({"packfile_type": "zip"}, "session1.zip"),
        ({"packfile_type": "zip", "packfile_name": "foo.zip"}, "foo.zip"),
    ],
)
def test_scan_with_template_strategy_w_packfile(packfile_opts, expected_packfile_name):
    walker = DummyWalker(
        [
            "test_project1/subject1/session1/1.dcm",
            "test_project1/subject1/session1/2.dcm",
        ]
    )

    tmpl = [
        {"pattern": "test_{project}"},
        {"pattern": "{subject}"},
    ]
    session_template = {"pattern": "{session}"}
    session_template.update(packfile_opts)
    tmpl.append(session_template)

    scanner = template.TemplateScanner(
        ingest_config=None,
        strategy_config=config.TemplateConfig(group="group_id", template=tmpl,),
        worker_config=None,
        walker=walker,
    )

    scan_results = list(scanner.scan("dir"))

    assert len(scan_results) == 1

    # match, item with type packfile
    item = scan_results[0]
    assert isinstance(item, s.Item)
    assert item.type == "packfile"
    assert item.dir == "/test_project1/subject1/session1"
    assert item.files == ["1.dcm", "2.dcm"]
    assert item.filename == expected_packfile_name


def test_scan_with_template_strategy_override(mocker):
    walker = DummyWalker(
        [
            "project1/subject1/session1/files/file.dcm",
            "project1/subject1/session1/files/file.txt",
            "subject1/file.dcm",
        ]
    )

    scanner = template.TemplateScanner(
        ingest_config=None,
        strategy_config=config.TemplateConfig(
            group="group_id",
            project="project",
            template=[
                {"pattern": "{project}"},
                {"pattern": "{subject}"},
                {"pattern": "{session}"},
                {"select": [{"pattern": ".*", "scan": "dicom"}]},
            ],
            group_override="group_override",
            project_override="project_override",
        ),
        worker_config=None,
        walker=walker,
    )

    scan_results = list(scanner.scan("dir"))

    assert len(scan_results) == 2

    # scan task
    task = scan_results[0]
    assert isinstance(task, s.TaskIn)
    assert task.type == "scan"
    assert task.context == {
        "group": {"_id": "group_id"},
        "project": {"label": "project1"},
        "subject": {"label": "subject1"},
        "session": {"label": "session1"},
        "scanner": {
            "type": "dicom",
            "dir": "/project1/subject1/session1/files",
            "opts": {},
        },
    }

    # item
    item = scan_results[1]
    assert isinstance(item, s.Item)
    assert item.type == "file"
    assert item.dir == "/subject1"
    assert item.files == ["file.dcm"]
    assert item.files_cnt == 1
    assert item.bytes_sum == 3
    assert item.context.dict(exclude_none=True) == {
        "group": {"id": "group_override"},
        "project": {"label": "project_override"},
    }


def test_scan_with_template_strategy_no_subject():
    walker = DummyWalker(["test_project1/session1/files/1.dcm",])

    scanner = template.TemplateScanner(
        ingest_config=None,
        strategy_config=config.TemplateConfig(
            group="group_id",
            template=[{"pattern": "test_{project}"}, {"pattern": "{session}"},],
            no_subjects=True,
        ),
        worker_config=None,
        walker=walker,
    )

    scan_results = list(scanner.scan("dir"))

    assert len(scan_results) == 1

    # match, item
    item = scan_results[0]
    assert isinstance(item, s.Item)
    assert item.type == "file"
    assert item.context.dict(exclude_none=True) == {
        "group": {"id": "group_id"},
        "project": {"label": "project1"},
        "subject": {"label": "session1"},
        "session": {"label": "session1"},
    }


def test_scan_with_dicom_strategy():
    walker = DummyWalker(["subj/session/acq/1.dcm"])

    scanner = template.TemplateScanner(
        ingest_config=None,
        strategy_config=config.DicomConfig(group="grp", project="prj"),
        worker_config=None,
        walker=walker,
    )

    scan_results = list(scanner.scan("foo"))
    assert len(scan_results) == 1

    task = scan_results[0]
    assert isinstance(task, s.TaskIn)
    assert task.type == "scan"
    assert task.context == {
        "group": {"_id": "grp"},
        "project": {"label": "prj"},
        "scanner": {"type": "dicom", "dir": "foo", "opts": {},},
    }
