from passlib.context import CryptContext

from src.application.service.auth.password import IPasswordService, PasswordService, AsyncBcryptService
from src.infrastructure.settings.stage.app import AppSettings


class PasswordServiceFactory:

    def __init__(self, app_settings: AppSettings):
        self.__app_settings = app_settings

    def create(self) -> IPasswordService:
        return PasswordService(AsyncBcryptService())
