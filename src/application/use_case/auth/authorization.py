from abc import ABC

from src.application.service.auth.jwt import IJwtService
from src.application.service.auth.password import IPasswordService
from src.application.service.user.crud import IUserCrudService
from src.domain.auth.exception.incorrect_password import PasswordIsIncorrectError


class IAuthorizationCase(ABC):
    pass


class AuthorizationCase(IAuthorizationCase):

    def __init__(
        self,
        user_crud_service: IUserCrudService,
        password_service: IPasswordService,
        jwt_service: IJwtService
    ):
        self.__user_crud = user_crud_service
        self.__password_service = password_service
        self.__jwt_service = jwt_service

    async def authorize(self, login: str, password: str) -> str:
        user = await self.__user_crud.read_by_login(login)

        if not self.__password_service.verify(password, user.password):
            raise PasswordIsIncorrectError("Некорректный пароль")

        return self.__jwt_service.create({
            "id": user.id,
            "login": user.login,
            "email": user.email,
            "roles": user.roles,
        })
