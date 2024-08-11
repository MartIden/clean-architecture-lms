from logging import Logger
from typing import NamedTuple, Type

from src.application.handler.interface import IHandler
from src.domain.common.dto.event import Event
from src.infrastructure.mediator.impl import Mediator
from src.infrastructure.mediator.interface import IMediator


class BindItem(NamedTuple):
    event: Type[Event]
    handler_factory: IHandler


class MediatorFactory:

    def __init__(self, logger: Logger, bindings: list[BindItem]) -> None:
        self.__logger = logger
        self.__bindings = bindings

    def create(self) -> IMediator:
        mediator = Mediator(self.__logger)

        for binding in self.__bindings:
            mediator.add_listener(binding.event, binding.handler_factory)

        return mediator
