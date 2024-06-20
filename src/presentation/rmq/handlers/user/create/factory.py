from src.infrastructure.kernel.rmq.handlers.factory_method import AbstractRmqHandlerCreator
from src.presentation.rmq.handlers.user.create.handler import CreateUserHandler


class CreateUserHandlerFactory(AbstractRmqHandlerCreator):

    def create(self) -> CreateUserHandler:
        return CreateUserHandler(
            self._message,
            self._di_container.core.logger()
        )
