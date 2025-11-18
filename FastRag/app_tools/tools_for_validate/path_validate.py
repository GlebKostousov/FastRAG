"""Module for path validation"""

from pathlib import Path

from config.custom_raises import PathValidateError

__all__ = ("validate_path_to_file",)


def validate_path_to_file(path_to_check: str | Path) -> Path:
    """
    Checks the path to the file. If the path is correct, it turns it into Path.

    Args:
        path_to_check (str, Path): path to check

    Returns:
        Path if the path is correct, otherwise raises

    Raises:
        PathValidateError: If the path is invalid.

    """
    try:
        result = Path(path_to_check)
    except (TypeError, ValueError) as e:
        msg = f"Unable to convert path: {path_to_check!r}. Error: {e}"
        raise PathValidateError(msg) from e

    if not result.exists():
        msg = f"File does not exist:{result}"
        raise PathValidateError(msg) from None

    if result.is_dir():
        msg = f"Path is a folder, expected file: {result}"
        raise PathValidateError(msg) from None

    return result
