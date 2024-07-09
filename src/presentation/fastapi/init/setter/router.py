from abc import ABC, abstractmethod
from dataclasses import dataclass

from fastapi import FastAPI, APIRouter, Depends

from src.presentation.fastapi.depends.request_json_logger import RequestJSONLoggerDepend
from src.presentation.fastapi.init.setter.interface import IAppSetter
from src.presentation.fastapi.router.docs import docs_api
from src.presentation.fastapi.router.urls import api_router


@dataclass
class RouterConfig:
    router: APIRouter
    kwargs: dict


class RoutersSetter(IAppSetter):

    def __init__(self, router_configs: list[RouterConfig]):
        self.__router_configs = router_configs

    def set(self, app: FastAPI) -> FastAPI:
        for router_config in self.__router_configs:
            app.include_router(router_config.router, **router_config.kwargs)
        return app


class IRoutersSetterFactory(ABC):
    @abstractmethod
    def create(self) -> IAppSetter: ...


class RoutersSetterFactory(IRoutersSetterFactory):

    __CONFIGS = [
        RouterConfig(router=api_router, kwargs={"dependencies": [Depends(RequestJSONLoggerDepend.log_it)]}),
        RouterConfig(router=docs_api, kwargs={"dependencies": [Depends(RequestJSONLoggerDepend.log_it)]}),
    ]

    def create(self) -> IAppSetter:
        return RoutersSetter(self.__CONFIGS)
