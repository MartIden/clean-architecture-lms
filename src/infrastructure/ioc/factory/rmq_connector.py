import asyncio

from src.infrastructure.settings.stage.app import AppSettings
from src.infrastructure.rmq.connector import (
    IRmqConnectorFactory,
    IRmqConnector,
    RmqConnectionSettings,
    RmqConnectorImpl
)


class RmqConnectorFactory(IRmqConnectorFactory):

    def __init__(self, settings: AppSettings):
        self.__settings = settings

    def create(self) -> IRmqConnector:
        loop = asyncio.get_event_loop()
        settings = RmqConnectionSettings(amqp_uri=self.__settings.RMQ_URI, loop=loop)
        return RmqConnectorImpl(settings)
