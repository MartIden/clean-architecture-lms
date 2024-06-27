from logging import Logger
from typing import Optional

from dependency_injector.wiring import Provide

from src import AppContainer
from src.application.use_case.user.creation import IUserCreationCase
from src.domain.user.dto.user import UserInCreate
from src.presentation.rmq.init.handlers.abstract_handler import AbstractRmqHandler


class CreateUserHandler(AbstractRmqHandler):

    def __init__(
        self,
        logger: Logger = Provide[AppContainer.core.logger],
        case: IUserCreationCase = Provide[AppContainer.services.user_creation_case]
    ):
        self._logger = logger
        self._case = case

    async def handle(self, message: dict, context: Optional[dict]) -> None:
        user = await self._case.create(UserInCreate(**message))
        self._logger.info(f"Created user {user.login}")
