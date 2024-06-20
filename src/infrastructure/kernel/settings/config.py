from functools import lru_cache
from typing import Dict, Type

from src.infrastructure.kernel.settings.stage.app import AppSettings
from src.infrastructure.kernel.settings.stage.base import AppEnvTypes, BaseAppSettings
from src.infrastructure.kernel.settings.stage.dev import DevAppSettings
from src.infrastructure.kernel.settings.stage.prod import ProdAppSettings
from src.infrastructure.kernel.settings.stage.test import TestAppSettings

environments: Dict[AppEnvTypes, Type[AppSettings]] = {
    AppEnvTypes.DEV: DevAppSettings,
    AppEnvTypes.PROD: ProdAppSettings,
    AppEnvTypes.TEST: TestAppSettings,
}


@lru_cache
def get_app_settings() -> AppSettings:
    app_env = BaseAppSettings().APP_ENV
    config = environments[app_env]
    return config()
