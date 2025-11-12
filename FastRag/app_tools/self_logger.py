"""Модуль кастомной настройки логирования."""

__all__ = ("LogConfig", "setup_logger")

import logging
import sys
from dataclasses import dataclass
from logging import Logger
from textwrap import fill

import colorama  # type: ignore[import]

from config.const import (
    COLOR_WHITE,
    DEFAULT_INDENT,
    DEFAULT_LEVEL,
    DEFAULT_MSG_WIDTH,
    LEVEL_COLORS,
    MODULE_NAME_WIDTH,
)


@dataclass(frozen=True, slots=True)
class LogConfig:
    """Конфигурация логирования."""

    msg_width: int = DEFAULT_MSG_WIDTH
    indent_length: int = DEFAULT_INDENT
    level: int = DEFAULT_LEVEL
    module_name_width: int = MODULE_NAME_WIDTH


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
        color = LEVEL_COLORS.get(level_name, COLOR_WHITE)

        message = fill(
            record.getMessage(),
            width=self._config.msg_width,
            subsequent_indent=" " * self._config.indent_length,
        )

        module_part = f"{self._module_name:<{self._config.module_name_width}}"
        formatted_msg = f"{color}{module_part}  {COLOR_WHITE}{message}"

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
