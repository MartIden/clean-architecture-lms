from functools import lru_cache
from typing import Dict, Type

from src.infrastructure.settings.stage.app import AppSettings
from src.infrastructure.settings.stage.base import AppEnvTypes, BaseAppSettings
from src.infrastructure.settings.stage.dev import DevAppSettings
from src.infrastructure.settings.stage.prod import ProdAppSettings
from src.infrastructure.settings.stage.test import TestAppSettings

environments: Dict[AppEnvTypes, Type[AppSettings]] = {
    AppEnvTypes.DEV: DevAppSettings,
    AppEnvTypes.PROD: ProdAppSettings,
    AppEnvTypes.TEST: TestAppSettings,
}


def get_app_settings() -> AppSettings:
    app_env = BaseAppSettings().APP_ENV
    config = environments[app_env]
    return config()
