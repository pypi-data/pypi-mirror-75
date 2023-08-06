from datetime import datetime
from unittest import mock

import pytest

from flywheel_cli import util
from flywheel_cli.ingest import config
from flywheel_cli.ingest import errors
from flywheel_cli.ingest import schemas as T
from flywheel_cli.ingest.scanners import dicom
from .conftest import AttrDict, DummyWalker


@pytest.fixture(scope="function")
def dummy_scanner():
    scanner = dicom.DicomScanner(
        ingest_config=config.IngestConfig(src_fs="/tmp"),
        strategy_config=None,
        worker_config=config.WorkerConfig(),
        walker=None,
        context={"group": {"_id": "group_id"}, "project": {"label": "project_label"},},
    )

    return scanner


@pytest.fixture(scope="function")
def data_for_session(mocker):
    dt = datetime(1900, 1, 2, 3, 4, 5)
    mocker.patch("flywheel_migration.dcm.DicomFile.timestamp", return_value=dt)

    context = {
        "group": {"_id": "group_id"},
        "project": {"label": "project_label"},
        "subject": {"label": "subject_label"},
        "session": {"label": "session_label"},
    }

    dcm = DCMattr_dict(
        {
            "StudyInstanceUID": "1",
            "PatientID": "patient_id",
            "StudyDate": "study_date",
            "StudyTime": "study_time",
            "SeriesDate": "series_date",
            "SeriesTime": "series_time",
            "_manufacturer": "SIEMENS",
        }
    )

    return context, dcm, dt


def test_scan(mocker, dummy_scanner):
    dcm = mock.Mock(
        **{
            "get": {
                "StudyInstanceUID": "1",
                "PatientID": "patient_id",
                "StudyDate": "19000102",
                "StudyTime": "030405",
                "SeriesDate": "19010101",
                "SeriesTime": "020304",
                "SeriesInstanceUID": "1.1",
                "AcquisitionNumber": "12",
                "SOPInstanceUID": "1.1.1",
            }.get,
            "get_manufacturer.return_value": "SIEMENS",
        }
    )

    mocker.patch("flywheel_cli.ingest.scanners.dicom.DicomFile", return_value=dcm)

    dummy_scanner.context = {
        "group": {"_id": "group_id"},
        "project": {"label": "project_label"},
        "subject": {"label": "subject_label"},
        "session": {"label": "session_label"},
    }
    dummy_scanner.walker = DummyWalker(["file1.dcm"])

    items = list(dummy_scanner.scan("path"))

    assert len(dummy_scanner.sessions) == 1

    assert len(dummy_scanner.sessions["1"].acquisitions) == 1
    assert len(items) == 1
    assert isinstance(items[0], T.ItemWithUIDs)
    item = items[0].item
    assert isinstance(item, T.Item)
    assert item.dir == "path/file1.dcm"
    assert item.context.dict(exclude_none=True) == {
        "group": {"id": "group_id"},
        "project": {"label": "project_label"},
        "subject": {"label": "subject_label"},
        "session": {
            "uid": "1",
            "label": "session_label",
            "timestamp": util.DEFAULT_TZ.localize(datetime(1900, 1, 2, 3, 4, 5)),
            "timezone": str(util.DEFAULT_TZ),
        },
        "acquisition": {
            "uid": "1.1",
            "label": "1901-01-01 02_03_04",
            "timestamp": util.DEFAULT_TZ.localize(datetime(1901, 1, 1, 2, 3, 4)),
            "timezone": str(util.DEFAULT_TZ),
        },
        "packfile": {"type": "dicom", "flatten": True},
    }
    assert len(items[0].uids) == 1
    uid = items[0].uids[0]
    assert isinstance(uid, T.UIDIn)
    assert uid.study_instance_uid == "1"
    assert uid.series_instance_uid == "1.1"
    assert uid.sop_instance_uid == "1.1.1"
    assert uid.acquisition_number == "12"
    assert uid.filename == "path/file1.dcm"
    assert uid.item_id == item.id


def test_scan_invalid_dicom(mocker, dummy_scanner):
    dcm_1 = mock.Mock(
        **{
            "get": {
                "StudyInstanceUID": "1",
                "PatientID": "patient_id",
                "SeriesInstanceUID": "1.1",
                "SOPInstanceUID": "1.1.1",
            }.get,
            "get_manufacturer.return_value": "SIEMENS",
        }
    )
    dcm_2 = mock.Mock(
        **{
            "get": {
                "SeriesInstanceUID": "1.1",
                "SOPInstanceUID": "1.1.1",
                "PatientID": "patient_id",
            }.get
        }
    )

    mocker.patch(
        "flywheel_cli.ingest.scanners.dicom.DicomFile", side_effect=[dcm_1, dcm_2]
    )
    dummy_scanner.walker = DummyWalker(["file1.dcm", "file2.dcm"])

    items = list(dummy_scanner.scan("path"))
    assert len(items) == 2
    item = items[0]
    assert isinstance(item, T.ItemWithUIDs)
    assert isinstance(item.item, T.Item)
    uids = item.uids
    assert isinstance(items[1], T.Error)
    error = items[1]
    assert error.code == errors.InvalidDicomFile.code
    assert error.message == "DICOM is missing StudyInstanceUID"
    assert error.filepath == "path/file2.dcm"


def test_scan_dicom_file(mocker, dummy_scanner):
    dcm_mock = mock.Mock(
        **{
            "get": {
                "StudyInstanceUID": "1",
                "PatientID": "patient_id",
                "SeriesDate": "19000102",
                "SeriesTime": "030405",
                "SeriesInstanceUID": "1.1",
                "SOPInstanceUID": "1.1.1",
            }.get,
            "get_manufacturer.return_value": "SIEMENS",
        }
    )

    mocker.patch("flywheel_cli.ingest.scanners.dicom.DicomFile", return_value=dcm_mock)

    dummy_scanner.context = {
        "group": {"_id": "group_id"},
        "project": {"label": "project_label"},
        "subject": {"label": "subject_label"},
        "session": {"label": "session_label"},
    }

    dummy_scanner.scan_dicom_file("path/file.dcm", None, [], 123)

    assert len(dummy_scanner.sessions) == 1
    assert len(dummy_scanner.sessions["1"].acquisitions) == 1
    assert dummy_scanner.sessions["1"].acquisitions["1.1"].context == {
        "acquisition": {
            "uid": "1.1",
            "label": "1900-01-02 03:04:05",
            "timestamp": util.DEFAULT_TZ.localize(datetime(1900, 1, 2, 3, 4, 5)),
            "timezone": str(util.DEFAULT_TZ),
        }
    }


def test_resolve_session_without_subject_code_fn(dummy_scanner, data_for_session):

    session = dummy_scanner.resolve_session(
        context=data_for_session[0], dcm=data_for_session[1]
    )

    assert isinstance(session, dicom.DicomSession)
    assert session.context == {
        "session": {
            "uid": "1",
            "label": "session_label",
            "timestamp": data_for_session[2],
            "timezone": str(util.DEFAULT_TZ),
        },
        "subject": {"label": "subject_label"},
    }

    assert session.acquisitions == {}
    assert session.secondary_acquisitions == {}
    assert len(dummy_scanner.sessions) == 1

    re_session = dummy_scanner.resolve_session(
        context=data_for_session[0], dcm=data_for_session[1]
    )
    assert len(dummy_scanner.sessions) == 1
    assert session == re_session


def test_resolve_acquisition_primary_no_related_acquisition(
    dummy_scanner, data_for_session
):
    context = data_for_session[0]
    context["acquisition"] = {"label": "acquisition_label"}

    dcm = data_for_session[1]
    dcm["SeriesInstanceUID"] = "1.1"

    acquisition = dummy_scanner.resolve_acquisition(context=context, dcm=dcm)

    assert isinstance(acquisition, dicom.DicomAcquisition)
    assert acquisition.context == {
        "acquisition": {
            "uid": "1.1",
            "label": "acquisition_label",
            "timestamp": data_for_session[2],
            "timezone": str(util.DEFAULT_TZ),
        }
    }

    assert acquisition.files == {}
    assert acquisition.filenames == {}

    assert len(dummy_scanner.sessions["1"].acquisitions) == 1
    assert len(dummy_scanner.sessions["1"].secondary_acquisitions) == 0
    assert dummy_scanner.sessions["1"].acquisitions["1.1"] == acquisition

    re_acquisition = dummy_scanner.resolve_acquisition(context=context, dcm=dcm)

    assert re_acquisition == acquisition
    assert len(dummy_scanner.sessions["1"].acquisitions) == 1
    assert len(dummy_scanner.sessions["1"].secondary_acquisitions) == 0
    assert dummy_scanner.sessions["1"].acquisitions["1.1"] == re_acquisition


def test_resolve_acquisition_related_acquisition(dummy_scanner, data_for_session):
    context = data_for_session[0]
    context["acquisition"] = {"label": "acquisition_label"}

    dcm = data_for_session[1]
    dcm["SeriesInstanceUID"] = "1.1"
    dcm["ReferencedFrameOfReferenceSequence"] = [
        {
            "RTReferencedStudySequence": [
                {"RTReferencedSeriesSequence": [{"SeriesInstanceUID": "1.1"}]}
            ]
        }
    ]
    dummy_scanner.related_acquisitions = True

    acquisition = dummy_scanner.resolve_acquisition(context=context, dcm=dcm)

    assert isinstance(acquisition, dicom.DicomAcquisition)
    assert acquisition.context == {
        "acquisition": {
            "uid": "1.1",
            "label": "acquisition_label",
            "timestamp": data_for_session[2],
            "timezone": str(util.DEFAULT_TZ),
        }
    }

    assert acquisition.files == {}
    assert acquisition.filenames == {}
    assert len(dummy_scanner.sessions["1"].acquisitions) == 0
    assert len(dummy_scanner.sessions["1"].secondary_acquisitions) == 1
    assert dummy_scanner.sessions["1"].secondary_acquisitions["1.1"] == acquisition


def test_resolve_session_with_subject_code_fn(mocker, attr_dict):
    dt = datetime(1900, 1, 2, 3, 4, 5)
    mocker.patch("flywheel_migration.dcm.DicomFile.timestamp", return_value=dt)

    subject_map = {}

    def subject_fn(fields):
        key = "".join(fields)
        return subject_map.setdefault(key, len(subject_map))

    fn = mock.Mock(side_effect=subject_fn)

    dcm = DCMattr_dict(
        {
            "StudyInstanceUID": "1",
            "PatientID": "patient_id1",
            "PatientName": "patient_name1",
            "StudyDate": "study_date",
            "StudyTime": "study_time",
            "SeriesDate": "series_date",
            "SeriesTime": "series_time",
            "_manufacturer": "SIEMENS",
        }
    )

    scanner = dicom.DicomScanner(
        ingest_config=config.IngestConfig(
            src_fs="/tmp",
            subject_config=config.SubjectConfig(
                code_serial=1,
                code_format="ex{SubjectCode}",
                map_keys=["PatientID", "PatientName"],
            ),
        ),
        strategy_config=None,
        worker_config=config.WorkerConfig(),
        walker=None,
        get_subject_code_fn=fn,
    )

    session = scanner.resolve_session(context=attr_dict({}), dcm=dcm)

    assert session.context == {
        "session": {
            "uid": "1",
            "label": "1900-01-02 03:04:05",
            "timestamp": dt,
            "timezone": str(util.DEFAULT_TZ),
        },
        "subject": {"label": 0},
    }

    assert subject_map["patient_id1patient_name1"] == 0
    fn.assert_called_once_with(["patient_id1", "patient_name1"])


def test_resolve_session_patient_id(mocker, attr_dict):
    dt = datetime(1900, 1, 2, 3, 4, 5)
    mocker.patch("flywheel_migration.dcm.DicomFile.timestamp", return_value=dt)

    dcm = DCMattr_dict(
        {
            "StudyInstanceUID": "1",
            "PatientID": "patient_id1",
            "PatientName": "patient_name1",
            "StudyDate": "study_date",
            "StudyTime": "study_time",
            "SeriesDate": "series_date",
            "SeriesTime": "series_time",
            "_manufacturer": "SIEMENS",
        }
    )

    scanner = dicom.DicomScanner(
        ingest_config=config.IngestConfig(src_fs="/tmp"),
        strategy_config=None,
        worker_config=config.WorkerConfig(),
        walker=None,
    )

    session = scanner.resolve_session(context=attr_dict({}), dcm=dcm)

    assert session.context == {
        "session": {
            "uid": "1",
            "label": "1900-01-02 03:04:05",
            "timestamp": dt,
            "timezone": str(util.DEFAULT_TZ),
        },
        "subject": {"label": "patient_id1"},
    }


def test_scan_dup_sop_uid(mocker, dummy_scanner):
    dcm_1 = mock.Mock(
        **{
            "get": {
                "StudyInstanceUID": "1",
                "PatientID": "patient_id",
                "SeriesInstanceUID": "1.1",
                "SOPInstanceUID": "1.1.1",
            }.get,
            "get_manufacturer.return_value": "SIEMENS",
        }
    )
    dcm_2 = mock.Mock(
        **{
            "get": {
                "StudyInstanceUID": "1",
                "PatientID": "patient_id",
                "SeriesInstanceUID": "1.1",
                "SOPInstanceUID": "1.1.1",
            }.get,
            "get_manufacturer.return_value": "SIEMENS",
        }
    )

    mocker.patch(
        "flywheel_cli.ingest.scanners.dicom.DicomFile", side_effect=[dcm_1, dcm_2]
    )
    dummy_scanner.walker = DummyWalker(["file1.dcm", "file2.dcm"])

    items = list(dummy_scanner.scan("path"))
    assert len(items) == 1
    item = items[0]
    assert isinstance(item, T.ItemWithUIDs)
    assert isinstance(item.item, T.Item)
    uids = item.uids
    assert len(uids) == 2

    file_paths = []
    for uid in uids:
        assert isinstance(uid, T.UIDIn)
        assert uid.study_instance_uid == "1"
        assert uid.series_instance_uid == "1.1"
        assert uid.sop_instance_uid == "1.1.1"
        file_paths.append(uid.filename)

    assert file_paths == ["path/file1.dcm", "path/file2.dcm"]


class DCMattr_dict(AttrDict):
    def get_manufacturer(self):
        return getattr(self, "_manufacturer")
