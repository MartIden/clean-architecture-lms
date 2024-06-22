from dependency_injector.wiring import inject, Provide

from src.infrastructure.ioc.container.application import ApplicationContainer
from src.infrastructure.settings.stage.app import AppSettings


__all__ = ["get_consumers"]

from src.presentation.rmq.consumers.user_new import UserNewConsumer

consumers = {
    "prod": [],
    "dev":  [
        UserNewConsumer,
    ],
    "test": [],
}


@inject
def get_consumers(app_settings: AppSettings = Provide[ApplicationContainer.core.settings]) -> list:
    env = app_settings.APP_ENV.value.lower()
    return consumers.get(env)
