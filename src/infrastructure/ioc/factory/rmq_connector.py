from asyncio import AbstractEventLoop

from src.infrastructure.settings.stage.app import AppSettings
from src.infrastructure.rmq.connector import (
    IRmqConnectorFactory,
    IRmqConnector,
    RmqConnectionSettings,
    RmqConnector
)


class RmqConnectorFactory(IRmqConnectorFactory):

    def __init__(self, settings: AppSettings, event_loop: AbstractEventLoop):
        self.__settings = settings
        self.__event_loop = event_loop

    def create(self) -> IRmqConnector:
        settings = RmqConnectionSettings(amqp_uri=self.__settings.RMQ_URI, event_loop=self.__event_loop)
        return RmqConnector(settings)
