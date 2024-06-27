from src.application.service.auth.jwt import IJwtService, JwtService
from src.infrastructure.settings.stage.app import AppSettings


class JwtServiceFactory:

    def __init__(self, app_settings: AppSettings):
        self.__app_settings = app_settings

    def create(self) -> IJwtService:
        return JwtService(
            algorithm=self.__app_settings.JWT_ALGORITHM,
            expiration_time=self.__app_settings.JWT_EXPIRATION_TIME,
            secret_key=self.__app_settings.JWT_SECRET_KEY
        )
