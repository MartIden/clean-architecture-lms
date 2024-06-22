from src.presentation.rmq.init.consumer import RmqHandlersRunnerConsumerImpl
from src.presentation.rmq.handlers.user.create.factory import CreateUserHandlerFactory


class UserNewConsumer(RmqHandlersRunnerConsumerImpl):

    _handlers_factories = [CreateUserHandlerFactory]

    async def _set_context(self) -> dict:
        return {
            "deal": {"id": 1}
        }

    @property
    def _queue_name(self) -> str:
        return "q.user.new"
