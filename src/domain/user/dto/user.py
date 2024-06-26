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


class UserInResponse(JsonModel):
    login: str
    email: str
    roles: list[UserRoleEnum]

    @classmethod
    def from_user(cls, user: User) -> "UserInResponse":
        return cls(
            login=user.login,
            email=user.email,
            roles=user.roles
        )
