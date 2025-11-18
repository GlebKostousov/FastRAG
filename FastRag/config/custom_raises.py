"""Module to keep app custom raises"""

__all__ = (
    "NotSafelyFileError",
    "PathValidateError",
)


class NotSafelyFileError(Exception):
    """Exception raised when a file is not safely for read"""


class PathValidateError(Exception):
    """Exception for path errors during validation"""
