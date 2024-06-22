from logging import Logger

from dependency_injector import containers, providers
from dependency_injector.providers import Factory

from src.infrastructure.ioc.factory.json_logger import JsonLoggerFactory
from src.infrastructure.settings.stage.app import AppSettings
from src.infrastructure.settings.config import get_app_settings


class CoreContainer(containers.DeclarativeContainer):
    settings: Factory[AppSettings] = providers.Callable(get_app_settings)
    logger: Factory[Logger] = providers.Callable(JsonLoggerFactory(name=__name__, settings=settings()).create)
