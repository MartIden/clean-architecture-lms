from dataclasses import dataclass

from src.domain.user.enum.roles import UserRoleEnum
from src.domain.user.value_object.login import UserLogin


@dataclass
class User:
    login: UserLogin
    email: UserEmail
    roles: list[UserRoleEnum]
