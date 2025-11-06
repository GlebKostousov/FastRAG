"""Модуль кастомной настройки логирования."""

__all__ = ("LogConfig", "setup_logger")

import logging
import sys
from dataclasses import dataclass
from logging import Logger
from textwrap import fill
from typing import Final

import colorama

_MODULE_NAME_WIDTH: Final[int] = 30
_COLOR_WHITE: Final[str] = colorama.Fore.WHITE
_DEFAULT_MSG_WIDTH: Final[int] = 110
_DEFAULT_INDENT: Final[int] = 36
_DEFAULT_LEVEL: Final[int] = logging.DEBUG
_LEVEL_COLORS: Final[dict[str, str]] = {
    "debug": colorama.Fore.BLUE,
    "info": colorama.Fore.CYAN,
    "warning": colorama.Fore.YELLOW,
    "error": colorama.Fore.LIGHTRED_EX,
    "critical": colorama.Fore.LIGHTMAGENTA_EX,
}


@dataclass(frozen=True, slots=True)
class LogConfig:
    """Конфигурация логирования."""

    msg_width: int = _DEFAULT_MSG_WIDTH
    indent_length: int = _DEFAULT_INDENT
    level: int = _DEFAULT_LEVEL
    module_name_width: int = _MODULE_NAME_WIDTH


class CustomFormatter(logging.Formatter):
    """Кастомный форматтер с цветами и выравниванием."""

    def __init__(
        self,
        module_name: str,
        config: LogConfig | None = None,
    ) -> None:
        """
        Инициализация класс

        Args:
            module_name (str): название модуля, инициализирующего лог
            config (LogConfig): настройка класса

        """
        super().__init__()
        self._module_name = module_name
        self._config = config or LogConfig()
        colorama.init(autoreset=True)

    def format(self, record: logging.LogRecord) -> str:
        """
        Переопределение модуля родителя, для кастомного форматирования

        Args:
            record (LogRecord): поступающий лог

        Returns:
            Форматированную строчку для лога

        """
        level_name = record.levelname.lower()
        color = _LEVEL_COLORS.get(level_name, _COLOR_WHITE)

        message = fill(
            record.getMessage(),
            width=self._config.msg_width,
            subsequent_indent=" " * self._config.indent_length,
        )

        module_part = f"{self._module_name:<{self._config.module_name_width}}"
        formatted_msg = f"{color}{module_part}  {_COLOR_WHITE}{message}"

        if record.exc_info:
            traceback_str = self.formatException(record.exc_info)
            return f"{formatted_msg}\n{traceback_str}"

        return formatted_msg


def setup_logger(
    module_name: str,
    path_to_log_file: str | None = None,
    config: LogConfig | None = None,
) -> Logger:
    """
    Настраивает логгер для модуля.

    Args:
        module_name: Имя модуля для идентификации в логах
        path_to_log_file: Путь к файлу для записи логов (опционально)
        config: Конфигурация логирования (опционально)

    Returns:
        Настроенный логгер

    """
    config = config or LogConfig()
    formated_logger: Logger = logging.getLogger(module_name)

    if formated_logger.hasHandlers():
        return formated_logger

    formated_logger.setLevel(config.level)

    console_handler = logging.StreamHandler(stream=sys.stdout)
    console_handler.setLevel(config.level)
    console_handler.setFormatter(
        CustomFormatter(module_name=module_name, config=config),
    )
    formated_logger.addHandler(console_handler)

    if path_to_log_file:
        file_handler = logging.FileHandler(path_to_log_file, encoding="utf-8")
        file_formatter = logging.Formatter(
            fmt="%(asctime)s - %(levelname)s - %(message)s",
        )
        file_handler.setFormatter(file_formatter)
        formated_logger.addHandler(file_handler)

    return formated_logger


if __name__ == "__main__":
    logger = setup_logger(__name__)
    logger.info("Log level: %d", logger.getEffectiveLevel())

    logger.debug("Инициализация системы завершена успешно.")
    logger.info("Загрузка BI отчетов по каждой структуре компании")
    logger.warning(
        "Следующие файлы не соответствуют шаблонам: %s",
        "20250221_132101.xlsx",
    )
    logger.error("Ошибка при загрузке данных! Проверьте исходные файлы.")
    logger.critical("Критическая ошибка: приложение не может продолжить работу.")
