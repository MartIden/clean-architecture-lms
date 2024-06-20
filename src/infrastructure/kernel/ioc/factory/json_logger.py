import logging
from typing import Optional

import json_log_formatter

from src.infrastructure.kernel.settings.stage.app import AppSettings


class JsonLoggerFactory:

    """Properties"""

    _json_formatter: Optional[json_log_formatter.JSONFormatter] = None
    _logging_level: Optional[int] = None
    _json_handler: Optional[logging.Handler] = None
    _json_logger: Optional[logging.Logger] = None

    def __init__(self, name: str, settings: AppSettings):
        self._name = name
        self._settings = settings

    @property
    def logging_level(self) -> int:
        if self._logging_level:
            return self._logging_level
        return self._settings.LOGGING_LEVEL

    @logging_level.setter
    def logging_level(self, logging_level: int) -> None:
        self._logging_level = logging_level

    @property
    def json_formatter(self) -> json_log_formatter.JSONFormatter:
        if self._json_formatter:
            return self._json_formatter

        self._json_formatter = json_log_formatter.VerboseJSONFormatter()
        return self._json_formatter

    @json_formatter.setter
    def json_formatter(self, json_formatter: json_log_formatter.JSONFormatter) -> None:
        self._json_formatter = json_formatter

    @property
    def json_handler(self) -> logging.Handler:
        if self._json_handler:
            return self._json_handler

        json_handler = logging.StreamHandler()
        json_handler.setFormatter(self.json_formatter)
        self._json_handler = json_handler

        return self._json_handler

    @json_handler.setter
    def json_handler(self, json_handler: logging.Handler) -> None:
        self._json_handler = json_handler

    def create(self) -> logging.Logger:
        if self._json_logger:
            return self._json_logger

        json_logger = logging.getLogger(self._name)
        json_logger.handlers = [self.json_handler]
        json_logger.setLevel(self.logging_level)

        return json_logger
