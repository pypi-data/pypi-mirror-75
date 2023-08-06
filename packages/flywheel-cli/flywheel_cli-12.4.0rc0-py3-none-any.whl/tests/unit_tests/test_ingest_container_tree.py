import io
import logging
import re
from uuid import UUID

import pytest

from flywheel_cli.ingest import schemas as s
from flywheel_cli.ingest.container_tree import ContainerNode, ContainerTree


@pytest.mark.parametrize(
    "node,expected",
    [
        (ContainerNode("foo"), "foo (creating)"),
        (ContainerNode("foo", existing=True), "foo (using)"),
        (ContainerNode("foo", bytes_sum=1024), "foo (1.0 KB) (creating)"),
        (
            ContainerNode("foo", bytes_sum=1024, files_cnt=1),
            "foo (1.0 KB / 1 file) (creating)",
        ),
        (
            ContainerNode("foo", bytes_sum=1024, files_cnt=2),
            "foo (1.0 KB / 2 files) (creating)",
        ),
    ],
)
def test_container_node_str_label(node, expected):
    assert str(node) == expected


def test_container_tree_add_node():
    container_1 = s.Container(
        id=UUID("00000000-0000-0000-0000-000000000000"),
        level=0,
        src_context={"label": "src_label"},
        path="src_label",
        dst_context={"_id": "000000000000000000000000", "label": "dst_label"},
    )

    tree = ContainerTree()

    # add first node
    tree.add_node(container_1)

    assert len(tree.nodes) == 1
    assert len(tree.root_nodes) == 1
    node_1 = tree.nodes[container_1.id]
    assert node_1.parent is None
    assert node_1 in tree.root_nodes
    assert node_1.label == "dst_label"
    assert node_1.bytes_sum == 0
    assert node_1.files_cnt == 0
    assert node_1.existing
    assert tree.total_files_cnt == 0
    assert tree.total_bytes_sum == 0

    container_2 = s.Container(
        id=UUID("00000000-0000-0000-0000-000000000002"),
        parent_id=UUID("00000000-0000-0000-0000-000000000000"),
        level=1,
        bytes_sum=1024,
        files_cnt=1,
        src_context={"label": "src_label"},
        path="group/src_label",
    )

    # add child container of the first one
    tree.add_node(container_2)

    assert len(tree.nodes) == 2
    assert len(tree.root_nodes) == 1
    node_2 = tree.nodes[container_2.id]
    assert node_2.parent == node_1
    assert node_2 not in tree.root_nodes
    assert node_2.label == "src_label"
    assert node_2.bytes_sum == 1024
    assert node_2.files_cnt == 1
    assert not node_2.existing
    assert tree.total_files_cnt == 1
    assert tree.total_bytes_sum == 1024
    assert len(node_1.children) == 1
    assert node_1.children[0] == node_2
    assert node_1.bytes_sum == 1024
    assert node_1.files_cnt == 0

    # adding node again is a noop
    tree.add_node(container_2)
    assert len(tree.nodes) == 2
    assert len(tree.root_nodes) == 1
    assert tree.total_files_cnt == 1
    assert tree.total_bytes_sum == 1024


def test_container_tree_add_node_child_before_parent(caplog):
    tree = ContainerTree()

    container = s.Container(
        id=UUID("00000000-0000-0000-0000-000000000002"),
        parent_id=UUID("00000000-0000-0000-0000-000000000000"),
        level=1,
        bytes_sum=1024,
        files_cnt=1,
        src_context={"label": "prj"},
        path="grp/prj",
    )

    tree.add_node(container)

    # skipped because parent node not in the added nodes
    assert len(tree.nodes) == 0
    assert len(tree.root_nodes) == 0
    # a warning is logged about the skippen container
    assert caplog.record_tuples == [
        (
            "flywheel_cli.ingest.container_tree",
            logging.WARNING,
            (
                "Couldn't find parent node for container: grp/prj. "
                "Probably trying to build container tree "
                "not in order (parent first then children). Skipping ..."
            ),
        )
    ]


def test_container_tree_print_not_utf8(tree_data):
    out = io.StringIO()
    tree_data.print_tree(out)
    out.seek(0)

    lines = [
        "`- label_1 (3.0 KB) (using)",
        "   |- label_1_1 (2.0 KB / 1 file) (creating)",
        "   |  `- label_1_1_1 (1.0 KB / 1 file) (creating)",
        "   `- label_1_2 (1.0 KB / 1 file) (creating)",
        "`- label_2 (creating)",
    ]

    print_lines = out.readlines()
    assert len(print_lines) == len(lines)
    for i in range(len(print_lines)):
        l = remove_color_formatting(print_lines[i]).rstrip()
        assert l == lines[i]


def test_container_tree_print_utf8(tree_data):
    out = UTF8StringIO()
    tree_data.print_tree(out)
    out.seek(0)

    lines = [
        "└─ label_1 (3.0 KB) (using)",
        "   ├─ label_1_1 (2.0 KB / 1 file) (creating)",
        "   │  └─ label_1_1_1 (1.0 KB / 1 file) (creating)",
        "   └─ label_1_2 (1.0 KB / 1 file) (creating)",
        "└─ label_2 (creating)",
    ]

    print_lines = out.readlines()
    assert len(print_lines) == len(lines)
    for i in range(len(print_lines)):
        l = remove_color_formatting(print_lines[i]).rstrip()
        assert l == lines[i]


@pytest.fixture(scope="function")
def tree_data():
    containers = [
        s.Container(
            id=UUID("00000000-0000-0000-0000-000000000000"),
            level=0,
            src_context={"label": "label_1"},
            path="label_1",
            dst_context={"_id": "000000000000000000000000", "label": "label_1"},
        ),
        s.Container(
            id=UUID("00000000-0000-0000-0000-000000000001"),
            level=0,
            src_context={"label": "label_2"},
            path="label_2",
        ),
        s.Container(
            id=UUID("00000000-0000-0000-0000-000000000002"),
            parent_id=UUID("00000000-0000-0000-0000-000000000000"),
            level=1,
            bytes_sum=1024,
            files_cnt=1,
            src_context={"label": "label_1_1"},
            path="label_1/label_1_1",
        ),
        s.Container(
            id=UUID("00000000-0000-0000-0000-000000000003"),
            parent_id=UUID("00000000-0000-0000-0000-000000000002"),
            level=2,
            bytes_sum=1024,
            files_cnt=1,
            src_context={"label": "label_1_1_1"},
            path="label_1/label_1_1/label_1_1_1",
        ),
        s.Container(
            id=UUID("00000000-0000-0000-0000-000000000004"),
            parent_id=UUID("00000000-0000-0000-0000-000000000000"),
            level=1,
            bytes_sum=1024,
            files_cnt=1,
            src_context={"label": "label_1_2"},
            path="label_1/label_1_2",
        ),
    ]

    tree = ContainerTree()
    for cont in containers:
        tree.add_node(cont)
    return tree


def remove_color_formatting(txt):
    """
    code from
    https://stackoverflow.com/questions/14693701/how-can-i-remove-the-ansi-escape-sequences-from-a-string-in-python
    """
    ansi_escape = re.compile(
        r"""
        \x1B  # ESC
        (?:   # 7-bit C1 Fe (except CSI)
            [@-Z\\-_]
        |     # or [ for CSI, followed by a control sequence
            \[
            [0-?]*  # Parameter bytes
            [ -/]*  # Intermediate bytes
            [@-~]   # Final byte
        )
    """,
        re.VERBOSE,
    )
    return ansi_escape.sub("", txt)


class UTF8StringIO(io.StringIO):
    encoding = "UTF-8"
