from flywheel_cli import errors


def test_auth_exception():
    ex = errors.AuthenticationError("message")
    assert isinstance(ex, errors.AuthenticationError)
    assert ex.code == 403

    ex = errors.AuthenticationError("message", 500)
    assert isinstance(ex, errors.AuthenticationError)
    assert ex.code == 500
