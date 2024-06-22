from enum import Enum
from pathlib import Path
from typing import Union

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppEnvTypes(Enum):
    PROD: Union["AppEnvTypes", str] = "prod"
    DEV:  Union["AppEnvTypes", str] = "dev"
    TEST: Union["AppEnvTypes", str] = "test"


class BaseAppSettings(BaseSettings):
    ROOT_DIR: Path = Path(__file__).parent.parent.parent.parent.parent.resolve()
    ENV_FILE: str = f'{ROOT_DIR}/.env'

    APP_ENV: AppEnvTypes = Field("prod", validation_alias="APP_ENV")

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding='utf-8',
        extra='allow'
    )
