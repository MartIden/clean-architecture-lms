from src.infrastructure.kernel.rmq.consumer import RmqHandlersRunnerConsumerImpl
from src.presentation.rmq.handlers.user.create.factory import CreateUserHandlerFactory


class UserNewConsumer(RmqHandlersRunnerConsumerImpl):

    _handlers_factories = [CreateUserHandlerFactory]

    @property
    def _queue_name(self) -> str:
        return "q.user.new"
