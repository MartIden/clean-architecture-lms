from abc import ABC, abstractmethod

from fastapi import FastAPI

from src.presentation.fastapi.init.event_handler.interface import IEventHandler
from src.presentation.fastapi.init.setters.interfase import IAppSetter


class EventHandlersSetter(IAppSetter):

    def __init__(self, handlers: list[IEventHandler]):
        self.__handlers = handlers

    def set(self, app: FastAPI) -> FastAPI:
        for handler in self.__handlers:
            app.add_event_handler(handler.event_type, handler.handle)
        return app


class IEventHandlersSetterFactory(ABC):
    @abstractmethod
    def create(self) -> IAppSetter: ...


class EventHandlersSetterFactory(IEventHandlersSetterFactory):
    def create(self) -> EventHandlersSetter:
        return EventHandlersSetter([])
