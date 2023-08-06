from unittest import mock

from flywheel_cli.commands.editions import _process_edition


def test_enable_lab_on_group(sdk_mock):
    args = mock.Mock()
    args.edition = "lab"
    args.group = "test_group"
    # We have to set to none or the mock will return a mock instance variable
    args.project = None

    sdk_mock.get_group.return_value = {}
    _process_edition(args, True)
    sdk_mock.modify_group.assert_called_with(args.group, {"editions": {"lab": True}})


def test_disable_lab_on_group(sdk_mock):
    args = mock.Mock()
    args.edition = "lab"
    args.group = "test_group"
    args.projects = None

    sdk_mock.get_group.return_value = {}
    _process_edition(args, False)
    sdk_mock.modify_group.assert_called_with(args.group, {"editions": {"lab": False}})


def test_enable_lab_on_project(sdk_mock):
    args = mock.Mock()
    args.edition = "lab"
    args.group = None
    args.project = "test_project"

    sdk_mock.get_project.return_value = {}
    _process_edition(args, True)
    sdk_mock.modify_project.assert_called_with(
        args.project, {"editions": {"lab": True}}
    )


def test_disable_lab_on_project(sdk_mock):
    args = mock.Mock()
    args.edition = "lab"
    args.group = None
    args.project = "test_project"

    sdk_mock.get_project.return_value = {}
    _process_edition(args, False)
    sdk_mock.modify_project.assert_called_with(
        args.project, {"editions": {"lab": False}}
    )


def test_enabling_new_edition_keeps_original_editions(sdk_mock):
    args = mock.Mock()
    args.edition = "lab"
    args.group = None
    args.project = "test_project"

    original_editions = {"original_val": True}
    expected_editions = {"original_val": True, "lab": True}

    sdk_mock.get_project.return_value.get.return_value = original_editions
    _process_edition(args, True)
    sdk_mock.modify_project.assert_called_with(
        args.project, {"editions": original_editions}
    )


def test_disabling_new_edition_keeps_original_editions(sdk_mock):
    args = mock.Mock()
    args.edition = "lab"
    args.group = None
    args.project = "test_project"

    original_editions = {"original_val": True}
    expected_editions = {"original_val": True, "lab": False}

    sdk_mock.get_project.return_value.get.return_value = original_editions
    _process_edition(args, False)
    sdk_mock.modify_project.assert_called_with(
        args.project, {"editions": expected_editions}
    )


def test_edition_invalid_edition_keeps_original_editions(sdk_mock):
    """This should never happen as the args parser does not allow invalid values
    but just in case we have a test to validate that it keeps the org editions as they were"""
    args = mock.Mock()
    args.edition = "DNE"
    args.group = None
    args.project = "test_project"

    original_editions = {"original_val": True}
    expected_editions = {"original_val": True, "DNE": True}

    sdk_mock.get_project.return_value.get.return_value = original_editions
    _process_edition(args, True)
    sdk_mock.modify_project.assert_called_with(
        args.project, {"editions": expected_editions}
    )
