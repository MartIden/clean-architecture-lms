from aio_pika.abc import AbstractIncomingMessage

from src.presentation.rmq.handlers.user.user_new_notify import CreateUserNotifyHandler
from src.presentation.rmq.init.consumer import RmqHandlersRunnerConsumer


class UserNewConsumer(RmqHandlersRunnerConsumer):

    _handlers_types = [CreateUserNotifyHandler]

    async def _set_context(self, message: AbstractIncomingMessage) -> dict:
        return {
            "deal": {"id": 1}
        }

    @property
    def _queue_name(self) -> str:
        return "q.user.new"
