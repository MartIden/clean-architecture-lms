from logging import Logger
from typing import Optional

from dependency_injector.wiring import Provide

from src import AppContainer
from src.domain.user.entity.user import User
from src.presentation.rmq.init.handlers.abstract_handler import AbstractRmqHandler


class CreateUserNotifyHandler(AbstractRmqHandler):

    def __init__(self, logger: Logger = Provide[AppContainer.core.logger]):
        self._logger = logger

    async def handle(self, message: dict, context: Optional[dict]) -> None:
        user = User.from_dict(message)
        self._logger.info(f"Send message to email {user.email}")
