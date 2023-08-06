import io
import shutil
import tempfile

import fs.path
import pytest

from flywheel_cli.folder_impl import FSWrapper
from flywheel_cli.importers.container_factory import ContainerNode


@pytest.fixture(scope="function")
def fs_wrapper():
    temp_dir = tempfile.mkdtemp()
    yield FSWrapper(temp_dir)
    shutil.rmtree(temp_dir)


def test_resolve_path(fs_wrapper):
    fs_wrapper.dst_fs.makedirs(fs.path.join("grp", "project_foo", "subject_bar"))

    # first param (container_type) is ignored
    path, _ = fs_wrapper.resolve_path(None, ["grp"])
    assert path == "grp"
    # replace non alphanumeric characters
    path, _ = fs_wrapper.resolve_path(None, ["grp", "project/foo", "subject:bar"])
    assert path == "grp/project_foo/subject_bar"
    path, _ = fs_wrapper.resolve_path(None, ["non_existent"])
    assert path is None


def test_create_container(fs_wrapper):
    group = ContainerNode("group", "grp/foo")
    path = fs_wrapper.create_container(None, group)
    assert path == "grp_foo"
    group.id = path

    project = ContainerNode("project", None, "project:bar")
    path = fs_wrapper.create_container(group, project)
    assert path == "grp_foo/project_bar"


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (ContainerNode("group", "grp_id"), "grp_id"),
        (ContainerNode("project", "project_id", "project_label"), "project_label"),
    ],
)
def test_path_el(test_input, expected, fs_wrapper):
    assert fs_wrapper.path_el(test_input) == expected


def test_upload_bytes(fs_wrapper):
    fs_wrapper.dst_fs.makedirs(fs.path.join("grp", "project", "subject"))
    subject = ContainerNode("subject", "grp/project/subject")

    fs_wrapper.upload(subject, "foo.txt", b"test_content")

    with fs_wrapper.dst_fs.open("grp/project/subject/foo.txt") as fp:
        assert fp.read() == "test_content"


def test_upload_file_like_obj(fs_wrapper):
    fs_wrapper.dst_fs.makedirs(fs.path.join("grp", "project", "subject"))
    subject = ContainerNode("subject", "grp/project/subject")

    fs_wrapper.upload(subject, "bar.txt", io.BytesIO(b"test_content"))

    with fs_wrapper.dst_fs.open("grp/project/subject/bar.txt") as fp:
        assert fp.read() == "test_content"
