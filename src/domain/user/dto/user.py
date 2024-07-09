from typing import Optional

from pydantic import UUID4

from src.domain.common.data_models import JsonModel
from src.domain.common.enum.order import Order
from src.domain.common.value_obj.limit import Limit
from src.domain.user.entity.user import User
from src.domain.user.enum.roles import UserRoleEnum
from src.domain.user.value_object.email import UserEmail
from src.domain.user.value_object.login import UserLogin
from src.domain.user.value_object.password import UserPassword


class UserInCreate(JsonModel):
    login:    UserLogin
    email:    UserEmail
    password: UserPassword
    roles:    list[UserRoleEnum]


class UserInLogin(JsonModel):
    login:    UserLogin
    password: UserPassword


class UserInUpdateRequest(JsonModel):
    login:    Optional[UserLogin] = None
    email:    Optional[UserEmail] = None
    password: Optional[UserPassword] = None
    roles:    Optional[list[UserRoleEnum]] = None


class UserInUpdate(JsonModel):
    id:       UUID4
    login:    Optional[UserLogin] = None
    email:    Optional[UserEmail] = None
    password: Optional[UserPassword] = None
    roles:    Optional[list[UserRoleEnum]] = None


class UserInResponse(JsonModel):
    id:    UUID4
    login: UserLogin
    email: UserEmail
    roles: list[UserRoleEnum]

    @classmethod
    def from_user(cls, user: User) -> Optional["UserInResponse"]:
        if user:
            return cls(
                id=user.id,
                login=user.login,
                email=user.email,
                roles=user.roles
            )


class UsersCountInResponse(JsonModel):
    count: int


class UserByCourseManyInRequest(JsonModel):
    id: UUID4
    limit:  Limit
    offset: int
    order:  Order
