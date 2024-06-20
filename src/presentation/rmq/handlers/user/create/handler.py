from logging import Logger

from src.infrastructure.kernel.rmq.handlers.abstract_handler import AbstractRmqHandler


class CreateUserHandler(AbstractRmqHandler):

    def __init__(self, message: dict, logger: Logger):
        self.__message = message
        self._logger = logger

    async def handle(self) -> None:
        self._logger.info("User created", extra=self.__message)
