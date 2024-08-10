from logging import Logger
from typing import NamedTuple, Type, Callable

from src.domain.common.dto.event import Event
from src.infrastructure.mediator.i_handler import IHandler
from src.infrastructure.mediator.mediator import IMediator, Mediator


class BindItem(NamedTuple):
    event: Type[Event]
    handler_factory: Callable[..., IHandler]


class MediatorFactory:

    def __init__(self, logger: Logger, bindings: list[BindItem]) -> None:
        self.__logger = logger
        self.__bindings = bindings

    def create(self) -> IMediator:
        mediator = Mediator(self.__logger)

        for binding in self.__bindings:
            mediator.bind(binding.event, binding.handler_factory)

        return mediator
