"""Module for storage app const"""

import logging
from enum import Enum
from pathlib import Path
from typing import Final

import colorama

__all__ = (
    "BASE_DIR_FASTRAG",
    "COLOR_WHITE",
    "DEFAULT_INDENT",
    "DEFAULT_LEVEL",
    "DEFAULT_MSG_WIDTH",
    "LEVEL_COLORS",
    "MODULE_NAME_WIDTH",
)

BASE_DIR_FASTRAG = Path(__file__).resolve().parent.parent

FILE_BLACKLIST = [
    "application/x-executable",
    "application/x-sharedlib",
    "application/x-dosexec",
]
SUSPICIOUS_EXTENSIONS = {".exe", ".dll", ".so", ".sh", ".bat"}
MODULE_NAME_WIDTH: Final[int] = 30
COLOR_WHITE: Final[str] = colorama.Fore.WHITE
DEFAULT_MSG_WIDTH: Final[int] = 110
DEFAULT_INDENT: Final[int] = 36
DEFAULT_LEVEL: Final[int] = logging.DEBUG
LEVEL_COLORS: Final[dict[str, str]] = {
    "debug": colorama.Fore.BLUE,
    "info": colorama.Fore.CYAN,
    "warning": colorama.Fore.YELLOW,
    "error": colorama.Fore.LIGHTRED_EX,
    "critical": colorama.Fore.LIGHTMAGENTA_EX,
}
DOCLING_ASR_MODEL: set[str] = {
    "tiny",
    "base",
    "small",
    "medium",
    "large",
    "turbo",
}


class Language(str, Enum):
    """Class for keep definition language options input file"""

    russia = "ru"
    english = "en"
