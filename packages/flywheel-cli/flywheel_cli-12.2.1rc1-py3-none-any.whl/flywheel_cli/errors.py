"""Flywheel CLI global errors"""

from typing import Optional


class BaseError(Exception):
    """Base exception"""

    message: str = "Unknown exception"

    def __init__(self, msg: Optional[str] = None):
        if msg:
            self.message = msg
        super().__init__(self.message)


class AuthenticationError(BaseError):
    """Authentication failed"""

    message: str = "Authentication error"
    code = 403

    def __init__(self, msg: str, code: Optional[int] = None):
        super().__init__(msg)
        if code:
            self.code = code


class NotEnoughPermissions(BaseError):
    """Permission error"""

    message: str = "The user does not have the required permissions for this action"
