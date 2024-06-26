from src.infrastructure.settings.config import get_app_settings

APP_SETTINGS = get_app_settings()
SQLALCHEMY_DATABASE_URL = APP_SETTINGS.POSTGRES_URI.replace("+asyncpg", "")
