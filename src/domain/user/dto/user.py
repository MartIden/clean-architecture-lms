from enum import Enum
from typing import Optional

from pydantic import UUID4, field_validator

from src.domain.common.data_models import JsonModel
from src.domain.user.entity.user import User
from src.domain.user.enum.roles import UserRoleEnum
from src.domain.user.value_object.email import UserEmail
from src.domain.user.value_object.login import UserLogin
from src.domain.user.value_object.password import UserPassword


class UserInCreate(JsonModel):
    login: UserLogin
    email: UserEmail
    password: UserPassword
    roles: list[UserRoleEnum]


class UserInUpdateRequest(JsonModel):
    login: Optional[UserLogin] = None
    email: Optional[UserEmail] = None
    password: Optional[UserPassword] = None
    roles: Optional[list[UserRoleEnum]] = None


class UserInUpdate(JsonModel):
    id: UUID4
    login: Optional[UserLogin] = None
    email: Optional[UserEmail] = None
    password: Optional[UserPassword] = None
    roles: Optional[list[UserRoleEnum]] = None


class UserInResponse(JsonModel):
    login: UserLogin
    email: UserEmail
    roles: list[UserRoleEnum]

    @classmethod
    def from_user(cls, user: User) -> "UserInResponse":
        return cls(
            login=user.login,
            email=user.email,
            roles=user.roles
        )


class UsersInResponse(JsonModel):
    rows: list[UserInResponse]
    count: int


class Order(str, Enum):
    asc = "ASC"
    desc = "DESC"


class UserManyInRequest(JsonModel):
    limit: int
    offset: int
    order: Order

    @field_validator("limit")
    def double(cls, v: int) -> int:
        assert v < 100
        return v
