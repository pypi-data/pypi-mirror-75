"""Shared errors."""
import attr


class DependencyError(Exception):
    pass


@attr.s(auto_attribs=True)
class ExitCodeError(Exception):
    """Raised when command returns non-zero exit code."""

    cmd: str
    return_code: str
    stderr: str
    stdout: str


class KMAError(Exception):
    pass


class DatabaseError(Exception):
    pass


class FileNotFoundError(Exception):
    """When file is not found."""

    pass


class CoordinateError(Exception):
    """Coordinate error major class."""
    pass


class CoordOutOfBoundsError(CoordinateError):
    """Coordinates related errors."""
    pass
