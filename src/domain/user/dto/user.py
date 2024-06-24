from dataclasses import dataclass

from src.domain.user.enum.roles import UserRoleEnum


@dataclass
class UserAnswer:
    login: str
    email: str


@dataclass
class UserInCreateRequest:
    login: str
    email: str
    password: str
    roles: list[UserRoleEnum]
