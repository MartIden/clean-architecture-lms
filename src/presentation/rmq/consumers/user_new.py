from src.presentation.rmq.handlers.user.create.handler import CreateUserHandler
from src.presentation.rmq.init.consumer import RmqHandlersRunnerConsumerImpl


class UserNewConsumer(RmqHandlersRunnerConsumerImpl):

    _handlers_types = [CreateUserHandler]

    async def _set_context(self) -> dict:
        return {
            "deal": {"id": 1}
        }

    @property
    def _queue_name(self) -> str:
        return "q.user.new"
