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

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        if data:
            return cls(
                id=data.get("id"),
                login=data.get("login"),
                email=data.get("email"),
                roles=data.get("roles"),
                password=data.get("password"),
            )
