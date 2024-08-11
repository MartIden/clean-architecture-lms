from logging import Logger
from typing import Any

from src.application.handler.interface import IHandler
from src.domain.common.dto.event import Event
from src.infrastructure.mediator.interface import IMediator


class Mediator(IMediator):

    def __init__(self, logger: Logger) -> None:
        self.__logger = logger
        self.__registry = {}

    def add_listener(self, event: type[Event], handler: IHandler) -> None:
        self.__registry[event] = handler

    def add_listeners(self, rows: tuple[type[Event], IHandler]) -> None:
        for row in rows:
            event, handler = row
            self.add_listener(event, handler)

    async def dispatch(self, event: Event) -> Any:
        try:
            handler = self.__registry[type(event)]
            return await handler(event)
        except IndexError:
            msg = f"Event {event.__class__.__name__} is not exist in current context"
            self.__logger.error(msg)
            raise Exception(msg)
        
    async def remove_listener(self, event: type[Event]) -> None:
        try:
            del self.__registry[event]
        except IndexError:
            msg = f"Event of {event.__class__.__name__} is not exist in current context"
            self.__logger.error(msg)
            return None
