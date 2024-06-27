from passlib.context import CryptContext

from src.application.service.auth.password import IPasswordService, PasswordService


class PasswordServiceFactory:
    @classmethod
    def create(cls) -> IPasswordService:
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return PasswordService(pwd_context)
