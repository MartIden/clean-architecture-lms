from typing import Annotated, Callable

from dependency_injector.providers import Factory
from dependency_injector.wiring import Provide
from fastapi import Depends, Header

from src.application.use_case.auth.authorization import IAuthorizationCase
from src.domain.auth.exception.header import AuthHeaderIsNotExistError
from src.domain.auth.exception.roles import RolesIncorrectError
from src.domain.user.entity.user import User
from src.domain.user.enum.roles import UserRoleEnum
from src.infrastructure.ioc.container.application import AppContainer


def get_token(authorization: Annotated[str, Header()],) -> str:
    if not authorization or "Bearer" not in authorization:
        raise AuthHeaderIsNotExistError("Отсутствует валидный заголовок авторизации")
    return authorization.replace("Bearer ", "")


async def get_current_user(
    token: str = Depends(get_token),
    auth_case_factory: Factory[IAuthorizationCase] = Depends(Provide[AppContainer.services.auth_case])
) -> User:
    auth_case = auth_case_factory.provider()
    return await auth_case.get_user_by_token(token)


def has_roles(roles: list[UserRoleEnum]) -> Callable:
    def role_validator(user: User = Depends(get_current_user)) -> User:
        if UserRoleEnum.ADMIN in user.roles:
            return user

        if not set(roles) & set(user.roles):
            raise RolesIncorrectError(f"У пользователя {user.login} нет требуемой роли")
        return user

    return role_validator
