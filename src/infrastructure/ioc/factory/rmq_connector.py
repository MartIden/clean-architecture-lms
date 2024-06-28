from src.infrastructure.settings.stage.app import AppSettings
from src.infrastructure.rmq.connector import (
    IRmqConnectorFactory,
    IRmqConnector,
    RmqConnectionSettings,
    RmqConnector
)


class RmqConnectorFactory(IRmqConnectorFactory):

    def __init__(self, settings: AppSettings):
        self.__settings = settings

    def create(self) -> IRmqConnector:
        settings = RmqConnectionSettings(amqp_uri=self.__settings.RMQ_URI)
        return RmqConnector(settings)
