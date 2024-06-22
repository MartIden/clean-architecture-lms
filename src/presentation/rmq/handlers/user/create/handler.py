from logging import Logger
from typing import Optional

from src.presentation.rmq.init.handlers.abstract_handler import AbstractRmqHandler


class CreateUserHandler(AbstractRmqHandler):

    def __init__(self, message: dict, logger: Logger):
        self.__message = message
        self._logger = logger

    async def handle(self, context: Optional[dict]) -> None:
        self._logger.info("Context", extra=context)
        self._logger.info("User created", extra=self.__message)
