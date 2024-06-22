from abc import ABC, abstractmethod
from typing import Any


from src.infrastructure.ioc.container.application import ApplicationContainer
from src.presentation.rmq.init.handlers.abstract_handler import AbstractRmqHandler


class AbstractRmqHandlerCreator(ABC):
    def __init__(
        self,
        message: Any,
        di_container: ApplicationContainer,
    ):
        self._message = message
        self._di_container = di_container

    @abstractmethod
    def create(self) -> AbstractRmqHandler:
        pass
