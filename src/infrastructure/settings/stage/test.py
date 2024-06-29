from pathlib import Path

from pydantic_settings import SettingsConfigDict

from src.infrastructure.settings.stage.app import AppSettings


class TestAppSettings(AppSettings):
    ROOT_DIR: Path = Path(__file__).parent.parent.parent.parent.parent.resolve()
    ENV_FILE: str = f'{ROOT_DIR}/test.env'

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding='utf-8',
        extra='allow'
    )
