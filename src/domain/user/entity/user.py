from pydantic import UUID4

from src.domain.common.entity import Entity
from src.domain.user.enum.roles import UserRoleEnum
from src.domain.user.value_object.email import UserEmail
from src.domain.user.value_object.login import UserLogin
from src.domain.user.value_object.password import UserPassword


class User(Entity[UUID4]):
    login: UserLogin
    email: UserEmail
    roles: list[UserRoleEnum]
    password: UserPassword | None = None
