from datetime import date, datetime
from unittest import mock

import flywheel
import pytest
import pytz
from flywheel_migration import deidentify
from pydicom.valuerep import MultiString

from flywheel_cli import models, errors, util


@pytest.fixture
def mocked_files():
    class TestFile:
        def __init__(self, name):
            self.name = name
            self.size = len(self.name)

    files = [TestFile(name) for name in ("a/b/c", "a/b/d", "a/e", "f",)]
    return files


@pytest.fixture(scope="function")
def default_auth_info():
    return models.FWAuth(
        api_key="api_key", host="host", user_id="user", is_admin=False, is_device=False,
    )


@pytest.mark.parametrize(
    "filename,expected",
    [
        ("test.dcm", True),
        ("test.DCM", True),
        ("test.dicom", True),
        ("test.DICOM", True),
        ("test.dcm.gz", True),
        ("test.DCM.GZ", True),
        ("test.dicom.gz", True),
        ("test.DICOM.GZ", True),
        ("/full/path/to/test.dcm", True),
        ("", False),
        ("/", False),
        ("/test.txt", False),
        ("/dcm.test", False),
        ("test.dcminst", False),
        ("test.dcm.zip", False),
    ],
)
def test_is_dicom_file(filename, expected):
    assert util.is_dicom_file(filename) == expected


def test_key_with_options():
    # Raises key error if key is missing
    with pytest.raises(KeyError):
        util.KeyWithOptions({})

    # String value
    opts = util.KeyWithOptions("value")
    assert opts.key == "value"
    assert opts.config == {}

    # Other value types
    opts = util.KeyWithOptions(4.2)
    assert opts.key == 4.2
    assert opts.config == {}

    # Dictionary with options
    opts = util.KeyWithOptions({"name": "Test Name", "option": 8.0})
    assert opts.key == "Test Name"
    assert opts.config == {"option": 8.0}

    # Dictionary with key override
    opts = util.KeyWithOptions({"pattern": "Test Pattern",}, key="pattern")
    assert opts.key == "Test Pattern"
    assert opts.config == {}


def test_get_filepath_dir_exists(mocker):
    mocker.patch("flywheel_cli.util.os.path.isdir", side_effect=[True])
    datetime_mock = mocker.patch("flywheel_cli.util.datetime.datetime")
    datetime_mock.utcnow.return_value = datetime(1900, 1, 1, 0, 0, 0)
    mocker.patch("flywheel_cli.util.get_cli_version", return_value="0.1.0.test")
    assert util.get_filepath("foo/") == "foo/log-19000101-000000-0.1.0.test.csv"


def test_get_filepath_dir_not_exists(mocker):
    mocker.patch("flywheel_cli.util.os.path.isdir", side_effect=[False])
    with pytest.raises(FileNotFoundError):
        util.get_filepath("foo/")


def test_get_incremental_filename(mocker):
    mocker.patch(
        "flywheel_cli.util.os.path.isfile", side_effect=[True, False, True, False]
    )
    assert util.get_incremental_filename("foo") == "foo(1)"
    assert util.get_incremental_filename("foo/bar(1).txt") == "foo/bar(2).txt"


@pytest.mark.parametrize(
    "seconds,expected",
    [
        (0, "0s"),
        (1, "1s"),
        (60, "1m"),
        (61, "1m 1s"),
        (3601, "1h"),
        (3660, "1h 1m"),
        (90000, "1d 1h"),
    ],
)
def test_hrtime(seconds, expected):
    assert util.hrtime(seconds) == expected


def test_create_missing_dirs_exists(mocker):
    makedirs_mock = mocker.patch("os.makedirs")

    with mock.patch("os.path.exists", return_value=True):
        util.create_missing_dirs("foo/bar")

    makedirs_mock.assert_not_called()


def test_create_missing_dirs_not_exists(mocker):
    makedirs_mock = mocker.patch("os.makedirs")

    with mock.patch("os.path.exists", return_value=False):
        util.create_missing_dirs("foo/bar")

    makedirs_mock.assert_called_once_with("foo")


@pytest.mark.parametrize(
    "iterable,chunk_size,expected",
    [
        ([], 1, []),
        ([1], 2, [[1]]),
        ([1, 2, 3, 4, 5], 2, [[1, 2], [3, 4], [5]]),
        (iter([1, 2, 3, 4, 5]), 4, [[1, 2, 3, 4], [5]]),
    ],
)
def test_chunks(iterable, chunk_size, expected):
    chunks = util.chunks(iterable, chunk_size)

    assert list(chunks) == expected


@pytest.mark.parametrize(
    "filenames,series_label,expected",
    [
        ({"id1": "label.dicom.zip"}, "label1", "label1.dicom.zip"),
        ({"id1": "label.dicom.zip"}, "label", "label_dup-1.dicom.zip"),
        (
            {"id1": "label.dicom.zip", "id2": "label_dup-1.dicom.zip"},
            "label",
            "label_dup-2.dicom.zip",
        ),
    ],
)
def test_dicom_utils_determine_dicom_zipname(filenames, series_label, expected):
    fname = util.DicomUtils.determine_dicom_zipname(
        filenames=filenames, series_label=series_label
    )
    assert fname == expected


@pytest.mark.parametrize(
    "context,dicom_dict,uid,timestamp,expected",
    [
        (
            {"session": {"label": "session01"}},
            {},
            "uid",
            datetime(1900, 1, 2, 3, 4, 5),
            "session01",
        ),  # context has the highest priority
        (
            {},
            {},
            "uid",
            datetime(1900, 1, 2, 3, 4, 5),
            "1900-01-02 03:04:05",
        ),  # next is the timestamp,
        ({}, {}, "uid", None, "uid"),  # last one is the uid
    ],
)
def test_dicom_utils_determine_session_label(
    context, dicom_dict, uid, timestamp, expected
):
    dicom_utils = util.DicomUtils()
    dcm_mock = mock.Mock(get=dicom_dict.get)

    label = dicom_utils.determine_session_label(
        context, dcm_mock, uid, timestamp=timestamp
    )

    assert label == expected


@pytest.mark.parametrize(
    "context,dicom_dict,uid,timestamp,expected",
    [
        (
            {"acquisition": {"label": "acq01"}},
            {"SeriesDescription": "Series Desc"},
            "uid",
            datetime(1900, 1, 2, 3, 4, 5),
            "acq01",
        ),  # context has the highest priority
        (
            {},
            {"SeriesDescription": "Series Desc"},
            "uid",
            datetime(1900, 1, 2, 3, 4, 5),
            "Series Desc",
        ),  # next is the SeriesDescription
        (
            {},
            {},
            "uid",
            datetime(1900, 1, 2, 3, 4, 5),
            "1900-01-02 03:04:05",
        ),  # next is the timestamp,
        ({}, {}, "uid", None, "uid"),  # last one is the uid
        (
            {},
            {"SeriesDescription": MultiString("foo\\bar")},
            None,
            None,
            "foo_bar",
        ),  # handles MultiValue
    ],
)
def test_dicom_utils_determine_acquisition_label(
    context, dicom_dict, uid, timestamp, expected
):
    dicom_utils = util.DicomUtils()
    dcm_mock = mock.Mock(get=dicom_dict.get)

    label = dicom_utils.determine_acquisition_label(
        context, dcm_mock, uid, timestamp=timestamp
    )

    assert label == expected


def test_dicom_utils_determine_acquisition_timestamp():
    dicom_utils = util.DicomUtils()
    dcm_mock = mock.Mock(
        **{
            "get": {
                "SeriesDate": "19990101",
                "SeriesTime": "102030",
                "AcquisitionDate": "20000101",
                "AcquisitionTime": "101112",
            }.get,
            "get_manufacturer.return_value": "SIEMENS",
        }
    )
    # siemens
    value = dicom_utils.determine_acquisition_timestamp(dcm=dcm_mock)
    assert value == util.DEFAULT_TZ.localize(datetime(1999, 1, 1, 10, 20, 30))

    # other manufacturer
    dcm_mock.get_manufacturer.return_value = "other"
    value = dicom_utils.determine_acquisition_timestamp(dcm=dcm_mock)
    assert value == util.DEFAULT_TZ.localize(datetime(2000, 1, 1, 10, 11, 12))


def test_dicom_utils_get_timestamp(mocker):
    dicom_utils = util.DicomUtils()
    dicom_mock = mocker.patch("flywheel_migration.dcm.DicomFile.timestamp")

    dicom_utils.get_timestamp(
        dcm={"date": "datevalue", "time": "timevalue"},
        date_key="date",
        time_key="time",
    )

    dicom_mock.assert_called_once_with("datevalue", "timevalue", util.DEFAULT_TZ)


def test_dicom_utils_get_value():
    dicom_utils = util.DicomUtils()
    dcm = mock.Mock(get={"key": "value", "empty_value": "", "zero": 0}.get)

    value = dicom_utils.get_value(dcm=dcm, key="key")
    assert value == "value"

    value = dicom_utils.get_value(dcm=dcm, key="key1")
    assert value is None

    value = dicom_utils.get_value(dcm=dcm, key="key1", default="default")
    assert value == "default"

    with pytest.raises(ValueError):
        value = dicom_utils.get_value(dcm=dcm, key="key1", required=True)

    with pytest.raises(ValueError):
        value = dicom_utils.get_value(dcm=dcm, key="empty_value", required=True)

    value = dicom_utils.get_value(dcm=dcm, key="zero", required=True)
    assert value == 0


def test_dicom_utils_get_value_with_deid_profile():
    profile = deidentify.DeIdProfile()
    profile.load_config(
        {
            "name": "test",
            "dicom": {
                "fields": [{"name": "PatientName", "replace-with": "Replaced Name"}]
            },
        }
    )
    dicom_profile = profile.get_file_profile("dicom")
    dicom_utils = util.DicomUtils(deid_profile=dicom_profile)

    dicom_dict = {
        "PatientName": "Patient Name",
        "PatientID": "Patient ID",
        "NoneField": None,
    }
    dcm = mock.Mock(get=dicom_dict.get, raw=mock.Mock(**dicom_dict))

    assert dicom_utils.get_value(dcm, "PatientName") == "Replaced Name"
    assert dicom_utils.get_value(dcm, "PatientID") == "Patient ID"
    # lastly check default value
    assert dicom_utils.get_value(dcm, "NoneField", "default") == "default"


@pytest.mark.parametrize(
    "context,dicom_dict,subject_code_fn,expected",
    [
        (
            {"subject": {"label": "sub01"}},
            {"PatientID": "Patient ID"},
            lambda _: "sub02",
            "sub01",
        ),  # context has the highest priority
        (
            {},
            {"PatientID": "Patient ID"},
            lambda _: "sub02",
            "sub02",
        ),  # subject code fn is the second
        (
            {},
            {"PatientID": "Patient ID"},
            None,
            "Patient ID",
        ),  # last one is the PatientID
    ],
)
def test_determine_subject_code(context, dicom_dict, subject_code_fn, expected):
    dicom_utils = util.DicomUtils(get_subject_code_fn=subject_code_fn)
    dcm = mock.Mock(get=dicom_dict.get)

    assert dicom_utils.determine_subject_code(context, dcm) == expected


@pytest.mark.parametrize(
    "context,dicom_dict,subject_code_fn,expected",
    [
        ({}, {}, None, util.InvalidLabel),  # no value in context nor in dicom file
        ({}, {}, lambda _: None, util.InvalidLabel),  # subject code fn return None
    ],
)
def test_determine_subject_code_raises(context, dicom_dict, subject_code_fn, expected):
    dicom_utils = util.DicomUtils(get_subject_code_fn=subject_code_fn)
    dcm = mock.Mock(get=dicom_dict.get)

    with pytest.raises(util.InvalidLabel):
        dicom_utils.determine_subject_code(context, dcm)


def test_encode_json_set():
    in_val = {"apple", "banana", "cherry"}

    ret_val = util.encode_json(in_val)

    assert set(ret_val) == in_val


def test_encode_json_date():
    in_val = date(2019, 2, 15)
    ret_val = util.encode_json(in_val)

    assert isinstance(ret_val, str)
    assert ret_val == "2019-02-15"


def test_encode_json_datetime_wo_tzinfo():
    in_val = datetime(2019, 2, 15, 10, 11, 12)

    ret_val = util.encode_json(in_val)

    assert isinstance(ret_val, str)
    assert ret_val == "2019-02-15T10:11:12+00:00"


def test_encode_json_datetime_w_tzinfo():
    in_val = pytz.timezone("Europe/Amsterdam").localize(
        datetime(2019, 2, 15, 10, 11, 12)
    )

    ret_val = util.encode_json(in_val)

    assert isinstance(ret_val, str)
    assert ret_val == "2019-02-15T09:11:12+00:00"


def test_json_serializer():
    in_val = {
        "a": {"a": "b"},
        "b": date(2019, 2, 15),
        "c": datetime(2019, 2, 15, 10, 11, 12),
        "d": 1,
    }

    ret_val = util.json_serializer(in_val)
    assert (
        ret_val
        == '{"a":{"a":"b"},"b":"2019-02-15","c":"2019-02-15T10:11:12+00:00","d":1}'
    )


def test_get_api_key_logged_out_raises(mocker):
    mocker.patch.object(util, "load_auth_config", return_value={})

    with pytest.raises(SystemExit):
        util.get_api_key()


def test_get_api_key_logged_in_returns_key(mocker):
    mocker.patch.object(util, "load_auth_config", return_value={"key": "apikey"})
    key = util.get_api_key()
    assert key == "apikey"


def test_get_upload_ticket_suggested_headers_empty_returns_none():
    response = {
        "ticket": "ticket",
        "headers": {},
        "urls": {"name": "url"},
    }
    headers = util.get_upload_ticket_suggested_headers(response)
    assert headers is None


def test_get_upload_ticket_suggested_headers_missing_returns_none():
    response = {
        "ticket": "ticket",
        "urls": {"name": "url"},
    }
    headers = util.get_upload_ticket_suggested_headers(response)
    assert headers is None


def test_get_upload_ticket_suggested_headers_not_dict_returns_none():
    response = {
        "ticket": "ticket",
        "headers": "bad-input",
        "urls": {"name": "url"},
    }
    headers = util.get_upload_ticket_suggested_headers(response)
    assert headers is None


def test_get_upload_ticket_suggested_headers_returns_headers():
    response = {
        "ticket": "ticket",
        "headers": {"x-test-header": "x-test-header-value"},
        "urls": {"name": "url"},
    }
    headers = util.get_upload_ticket_suggested_headers(response)
    assert headers is not None
    assert len(headers.keys()) == 1
    assert headers["x-test-header"] == "x-test-header-value"


def test_sdk_client_init(mocker):
    flywheel_mock = mocker.patch("flywheel.Client")

    sdk = util.SDKClient("api:key")

    flywheel_mock.assert_called_once_with("api:key")
    assert isinstance(sdk, util.SDKClient)


def test_sdk_client_init_invalid_api_key_format_raise():
    with pytest.raises(errors.AuthenticationError):
        util.SDKClient("foo-bar")


def test_sdk_client_call_api_no_kwargs(mocker):
    flywheel_mock = mocker.patch("flywheel.Client")

    sdk = util.SDKClient("api:key")

    sdk.call_api("/path", "GET")
    flywheel_mock.return_value.api_client.call_api.assert_called_once_with(
        "/path",
        "GET",
        _preload_content=True,
        _return_http_data_only=True,
        auth_settings=["ApiKey"],
    )


def test_sdk_client_call_api_with_kwargs(mocker):
    flywheel_mock = mocker.patch("flywheel.Client")

    sdk = util.SDKClient("api:key")

    sdk.call_api(
        "/path",
        "GET",
        _preload_content=False,
        auth_settings=["Custom"],
        not_default="value",
    )
    flywheel_mock.return_value.api_client.call_api.assert_called_once_with(
        "/path",
        "GET",
        _preload_content=False,
        _return_http_data_only=True,
        auth_settings=["Custom"],
        not_default="value",
    )


def test_sdk_client_create_upload_ticket(mocker):
    flywheel_mock = mocker.patch("flywheel.Client")
    flywheel_mock.return_value.api_client.call_api.return_value = {
        "ticket": "ticketid",
        "urls": {"filename": "fileurl"},
    }

    sdk = util.SDKClient("api:key")

    response = sdk.create_upload_ticket("/url", "filename")
    assert response == ("ticketid", "fileurl", None)

    flywheel_mock.return_value.api_client.call_api.assert_called_once_with(
        "/url",
        "POST",
        _preload_content=True,
        _return_http_data_only=True,
        auth_settings=["ApiKey"],
        body={"metadata": {}, "filenames": ["filename"]},
        query_params=[("ticket", "")],
        response_type=object,
    )

    flywheel_mock.reset_mock()

    response = sdk.create_upload_ticket("/url", "filename", {"meta": "data"})
    assert response == ("ticketid", "fileurl", None)

    flywheel_mock.return_value.api_client.call_api.assert_called_once_with(
        "/url",
        "POST",
        _preload_content=True,
        _return_http_data_only=True,
        auth_settings=["ApiKey"],
        body={"metadata": {"meta": "data"}, "filenames": ["filename"]},
        query_params=[("ticket", "")],
        response_type=object,
    )


def test_sdk_client_signed_url_upload(mocker):
    flywheel_mock = mocker.patch("flywheel.Client")
    flywheel_mock.return_value.api_client.call_api.return_value = {
        "ticket": "ticketid",
        "urls": {"filename": "fileurl"},
    }
    file = mock.Mock()

    sdk = util.SDKClient("api:key")

    sdk.signed_url_upload("cont_name", "cont_id", "filename", file, {"meta": "meta"})

    flywheel_mock.return_value.api_client.call_api.assert_has_calls(
        [
            mock.call(
                "/cont_names/cont_id/files",
                "POST",
                _preload_content=True,
                _return_http_data_only=True,
                auth_settings=["ApiKey"],
                body={"metadata": {"meta": "meta"}, "filenames": ["filename"]},
                query_params=[("ticket", "")],
                response_type=object,
            ),
            mock.call(
                "/cont_names/cont_id/files",
                "POST",
                _preload_content=True,
                _return_http_data_only=True,
                auth_settings=["ApiKey"],
                query_params=[("ticket", "ticketid")],
            ),
        ]
    )


def test_sdk_client_upload_not_signed(mocker):
    flywheel_mock = mocker.patch("flywheel.Client")
    mocker.patch("os.fstat", **{"return_value.st_size": 10})
    uploader = mock.Mock()
    filespec = mock.Mock()
    flywheel_mock.return_value.upload_file_to_cont_name = uploader
    filespec_mock = mocker.patch("flywheel.FileSpec", return_value=filespec)
    file_mock = mock.MagicMock()

    sdk = util.SDKClient("api:key")
    sdk.signed_url = False

    sdk.upload("cont_name", "cont_id", "filename", file_mock, {"meta": "meta"})

    filespec_mock.assert_called_once_with(
        "filename", file_mock,
    )

    uploader.assert_called_once_with("cont_id", filespec, metadata='{"meta":"meta"}')


def test_sdk_client_is_logged_in_invalid_api_key_raise(mocker):
    flywheel_mock = mocker.patch("flywheel.Client")
    flywheel_mock.return_value.get_auth_status.side_effect = flywheel.ApiException(
        status=401, reason="Foo"
    )

    sdk = util.SDKClient("api:key")

    with pytest.raises(errors.AuthenticationError) as execinfo:
        sdk.is_logged_in()

    assert execinfo.value.args[0] == "Foo"
    assert execinfo.value.code == 401


def test_sdk_client_can_import_into_wo_group_wo_project(mocker):
    fw_mock = mocker.patch("flywheel.Client").return_value
    sdk = util.SDKClient("api:key")

    sdk.can_import_into(None, None)

    fw_mock.lookup.assert_not_called()


def test_sdk_client_can_import_into_wo_group_w_project(mocker):
    fw_mock = mocker.patch("flywheel.Client").return_value
    sdk = util.SDKClient("api:key")

    sdk.can_import_into(None, "project")

    fw_mock.lookup.assert_not_called()


def test_sdk_client_can_import_into_w_group_403(mocker):
    fw_mock = mocker.patch("flywheel.Client").return_value
    fw_mock.lookup.side_effect = flywheel.ApiException(status=403)
    sdk = util.SDKClient("api:key")

    with pytest.raises(errors.NotEnoughPermissions) as excinfo:
        sdk.can_import_into("group")

    assert excinfo.value.message == "User does not have access to 'group'"


def test_sdk_client_can_import_into_w_group_500(mocker):
    fw_mock = mocker.patch("flywheel.Client").return_value
    fw_mock.lookup.side_effect = flywheel.ApiException(status=500)
    sdk = util.SDKClient("api:key")

    # re-raise exception if status is not 403/404
    with pytest.raises(flywheel.ApiException) as excinfo:
        sdk.can_import_into("group")


def test_sdk_client_can_import_into_w_group_404_non_admin(mocker, default_auth_info):
    fw_mock = mocker.patch("flywheel.Client").return_value
    fw_mock.lookup.side_effect = flywheel.ApiException(status=404)
    sdk = util.SDKClient("api:key")
    sdk._auth_info = default_auth_info

    with pytest.raises(errors.NotEnoughPermissions) as excinfo:
        sdk.can_import_into("group")

    assert excinfo.value.message == "User does not have access to create 'group'"


def test_sdk_client_can_import_into_w_group_404_admin(mocker, default_auth_info):
    fw_mock = mocker.patch("flywheel.Client").return_value
    fw_mock.lookup.side_effect = flywheel.ApiException(status=404)
    sdk = util.SDKClient("api:key")
    sdk._auth_info = default_auth_info
    sdk._auth_info.is_admin = True

    sdk.can_import_into("group")


def test_sdk_client_can_import_into_w_group_200_wo_project(mocker, default_auth_info):
    mocker.patch("flywheel.Client")
    sdk = util.SDKClient("api:key")
    sdk._auth_info = default_auth_info

    sdk.can_import_into("group")


def test_sdk_client_can_import_into_w_group_w_project_403(mocker, default_auth_info):
    fw_mock = mocker.patch("flywheel.Client").return_value
    fw_mock.lookup.side_effect = [mock.Mock(), flywheel.ApiException(status=403)]
    sdk = util.SDKClient("api:key")

    with pytest.raises(errors.NotEnoughPermissions) as excinfo:
        sdk.can_import_into("group", "project")

    assert excinfo.value.message == "User does not have access to 'group/project'"


def test_sdk_client_can_import_into_w_group_w_project_500(mocker):
    fw_mock = mocker.patch("flywheel.Client").return_value
    fw_mock.lookup.side_effect = [mock.Mock(), flywheel.ApiException(status=500)]
    sdk = util.SDKClient("api:key")

    with pytest.raises(flywheel.ApiException) as excinfo:
        sdk.can_import_into("group", "project")


def test_sdk_client_can_import_into_w_group_w_project_404_non_grp_admin(
    mocker, default_auth_info
):
    fw_mock = mocker.patch("flywheel.Client").return_value
    group_mock = mock.Mock(permissions=[mock.Mock(id="user", access="read-only")])
    fw_mock.lookup.side_effect = [group_mock, flywheel.ApiException(status=404)]
    sdk = util.SDKClient("api:key")
    sdk._auth_info = default_auth_info

    with pytest.raises(errors.NotEnoughPermissions) as excinfo:
        sdk.can_import_into("group", "project")

    assert (
        excinfo.value.message == "User does not have access to create 'group/project'"
    )


def test_sdk_client_can_import_into_w_group_w_project_404_grp_admin(
    mocker, default_auth_info
):
    fw_mock = mocker.patch("flywheel.Client").return_value
    group_mock = mock.Mock(permissions=[mock.Mock(id="user", access="admin")])
    fw_mock.lookup.side_effect = [group_mock, flywheel.ApiException(status=404)]
    sdk = util.SDKClient("api:key")
    sdk._auth_info = default_auth_info

    sdk.can_import_into("group", "project")


def test_sdk_client_can_import_into_w_group_w_project_200_missing_actions(
    mocker, default_auth_info
):
    fw_mock = mocker.patch("flywheel.Client").return_value
    project_mock = mock.Mock(permissions=[mock.Mock(id="user", role_ids=["a", "b"])])
    fw_mock.lookup.side_effect = [mock.Mock(), project_mock]
    fw_mock.get_role.return_value = mock.Mock(actions=["containers_create_hierarchy"])
    sdk = util.SDKClient("api:key")
    sdk._auth_info = default_auth_info

    with pytest.raises(errors.NotEnoughPermissions) as excinfo:
        sdk.can_import_into("group", "project")

    assert excinfo.value.message == (
        "User does not have the required permissions "
        "(containers_create_hierarchy, files_create_upload) in 'project' project. "
        "Missing permissions: files_create_upload"
    )


def test_sdk_client_can_import_into_w_group_w_project_200_has_actions(
    mocker, default_auth_info
):
    fw_mock = mocker.patch("flywheel.Client").return_value
    project_mock = mock.Mock(permissions=[mock.Mock(id="user", role_ids=["a", "b"])])
    fw_mock.lookup.side_effect = [mock.Mock(), project_mock]
    fw_mock.get_role.return_value = mock.Mock(
        actions=["containers_create_hierarchy", "files_create_upload"]
    )
    sdk = util.SDKClient("api:key")
    sdk._auth_info = default_auth_info

    sdk.can_import_into("group", "project")


def test_get_path_el_group():
    ret_val = util.get_path_el(c_type="group", context={"_id": "id", "label": "label"})
    assert ret_val == "id"

    ret_val = util.get_path_el(
        c_type="group", context={"_id": "id", "label": "label"}, use_labels=True
    )
    assert ret_val == "id"


def test_get_path_el_full_context():
    ret_val = util.get_path_el(c_type="none", context={"_id": "id", "label": "label"})
    assert ret_val == "<id:id>"

    ret_val = util.get_path_el(
        c_type="none", context={"_id": "id", "label": "label"}, use_labels=True
    )
    assert ret_val == "label"


def test_get_path_el_partial_context():
    ret_val = util.get_path_el(c_type="none", context={"_id": None, "label": "label"})
    assert ret_val == "label"

    ret_val = util.get_path_el(c_type="none", context={"label": "label"})
    assert ret_val == "label"


def test_get_path_el_no_info_raises():
    with pytest.raises(TypeError):
        util.get_path_el(c_type="none", context={"no": "key"})

    with pytest.raises(TypeError):
        util.get_path_el(c_type="none", context={"no": "key"}, use_labels=True)

    with pytest.raises(TypeError):
        util.get_path_el(c_type="none", context={"_id": "id"}, use_labels=True)

    with pytest.raises(TypeError):
        util.get_path_el(
            c_type="none", context={"_id": "id", "label": None}, use_labels=True
        )


def test_lru_cache_maxsize():
    cache = util.LRUCache(maxsize=2)

    cache["key1"] = "value1"
    cache["key2"] = "value2"

    assert cache["key1"] == "value1"
    assert cache["key2"] == "value2"
    assert len(cache.cache) == 2

    cache["key3"] = "value3"
    assert len(cache.cache) == 2

    with pytest.raises(KeyError):
        cache["key1"]
    assert cache["key2"] == "value2"
    assert cache["key3"] == "value3"


def test_lru_cache_get_w_default_value():
    cache = util.LRUCache(maxsize=2)
    cache["key1"] = "value1"

    assert cache.get("key1") == "value1"
    assert cache.get("key1", "default") == "value1"
    assert cache.get("key2", "default") == "default"

    with pytest.raises(KeyError):
        cache["key2"]


@pytest.mark.parametrize(
    "path,paths,result",
    [
        ("path/file.txt", ["path/file.txt"], "path/file_1.txt"),
        ("path/file.txt", ["path/file.txt", "path/file_1.txt"], "path/file_2.txt"),
        (
            "path/other/file.random.ext.txt",
            ["path/other/file.random.ext.txt"],
            "path/other/file.random_1.ext.txt",
        ),
    ],
)
def test_create_unique_filename(path, paths, result):
    safe_name = util.create_unique_filename(path, paths)
    assert safe_name == result
