from abc import ABC, abstractmethod

from src.application.service.auth.password import IPasswordService
from src.application.service.user.crud import IUserCrudService
from src.domain.common.ports.publisher import IPublisher
from src.domain.user.dto.user import UserInCreate
from src.domain.user.entity.user import User


class IUserCreationCase(ABC):
    @abstractmethod
    async def create(self, user: UserInCreate) -> User: ...


class UserCreationCase(IUserCreationCase):

    def __init__(
        self,
        password_service: IPasswordService,
        user_crud_service: IUserCrudService,
        user_publisher: IPublisher,
    ):
        self.__password_service = password_service
        self.__user_crud_service = user_crud_service
        self.__user_publisher = user_publisher

    def __create_user_with_hash(self, user: UserInCreate) -> UserInCreate:
        return UserInCreate(
            login=user.login,
            email=user.email,
            roles=user.roles,
            password=self.__password_service.hash(user.password),
        )

    async def create(self, user: UserInCreate) -> User:
        user = await self.__user_crud_service.create(data=self.__create_user_with_hash(user))
        await self.__user_publisher.publish_model(user)
        return user
