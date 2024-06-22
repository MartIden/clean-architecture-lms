from dependency_injector.wiring import Provide, inject
from starlette.middleware.cors import CORSMiddleware

from src.infrastructure.ioc.container.application import AppContainer
from src.infrastructure.settings.stage.app import AppSettings
from src.presentation.fastapi.init.setter.handler.middleware.interface import IMiddlewareHandler


class CorsMiddlewareHandler(IMiddlewareHandler):

    @inject
    def __init__(self, app_settings: AppSettings = Provide[AppContainer.core.settings]):
        self.__app_settings = app_settings

    @property
    def middleware_class(self) -> type:
        return CORSMiddleware

    @property
    def kwargs(self) -> dict:
        return {
            "allow_origins": self.__app_settings.ALLOWED_HOSTS,
            "allow_methods": ["*"],
            "allow_headers": ["*"],
        }
