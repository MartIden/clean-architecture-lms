from src.presentation.rmq.handlers.user.create.handler import CreateUserHandler
from src.presentation.rmq.init.handlers.factory_method import AbstractRmqHandlerCreator


class CreateUserHandlerFactory(AbstractRmqHandlerCreator):

    def create(self) -> CreateUserHandler:
        return CreateUserHandler(
            self._message,
            self._di_container.core.logger()
        )
