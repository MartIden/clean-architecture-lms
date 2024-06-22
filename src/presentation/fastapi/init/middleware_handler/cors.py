from dependency_injector.wiring import Provide
from starlette.middleware.cors import CORSMiddleware

from src.infrastructure.ioc.container.application import ApplicationContainer
from src.infrastructure.settings.stage.app import AppSettings
from src.presentation.fastapi.init.middleware_handler.interface import IMiddlewareHandler


class CorsMiddlewareHandler(IMiddlewareHandler):

    def __init__(self, app_settings: AppSettings = Provide[ApplicationContainer.core.settings]):
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
