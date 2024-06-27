from typing import Any, Dict, List, Optional

from pydantic import Field

from src.infrastructure.settings.stage.base import BaseAppSettings
from src.infrastructure.settings.unit.rmq_migration import RmqMigrationSettings
from src.presentation.rmq.init.migrations_map import get_migration_settings


class AppSettings(BaseAppSettings):

    """ FASTAPI """
    DEBUG: bool = False
    DOCS_URL: str | None = "/docs"
    OPENAPI_PREFIX: str = ""
    OPENAPI_URL: Optional[str] = None
    REDOC_URL: str | None = None
    TITLE: str = "lms"
    VERSION: str = "0.0.1"
    HOST: str = Field("0.0.0.0", validation_alias="HOST")
    PORT: int = Field(5005, validation_alias="PORT")
    RELOAD: bool = Field(True, validation_alias="RELOAD")

    """ DOC_AUTH """
    DOC_LOGIN: str = "admin"
    DOC_PASS: str = "s#d23x4&*d32"

    """POSTGRES SETTINGS"""
    POSTGRES_SCHEMA: str = Field(..., validation_alias="POSTGRES_SCHEME")
    POSTGRES_URI: str = Field(..., validation_alias="POSTGRES_URI")

    """ RMQ SETTINGS """
    RMQ_MIGRATION_SETTINGS: RmqMigrationSettings = Field(
        get_migration_settings(), validation_alias="RMQ_MIGRATION_SETTINGS"
    )

    RMQ_URI: str = Field(..., validation_alias="RMQ_URI")

    """ JWT """
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_TIME: int = 30 * 24 * 60 * 60
    JWT_SECRET_KEY: str = "8q%32h1[_3bB~yg]6#i"

    MAX_CONNECTION: int = 10
    SALT: str = "R6^,)7^$==sOT@hs0"
    SHOW_TRACEBACK_IN_RESPONSE: bool = Field(False, validation_alias="SHOW_TRACEBACK_IN_RESPONSE")

    ALLOWED_HOSTS: List[str] = [
        "*",
    ]

    LOGGING_LEVEL: int = Field(20, validation_alias="LOGGING_LEVEL")
    FASTAPI_LOGGING_LEVEL: int = Field(50, validation_alias="FASTAPI_LOGGING_LEVEL")

    @property
    def fastapi_kwargs(self) -> Dict[str, Any]:
        return {
            "debug": self.DEBUG,
            "docs_url": self.DOCS_URL,
            "openapi_prefix": self.OPENAPI_PREFIX,
            "openapi_url": self.OPENAPI_URL,
            "redoc_url": self.REDOC_URL,
            "title": self.TITLE,
            "version": self.VERSION,
        }
