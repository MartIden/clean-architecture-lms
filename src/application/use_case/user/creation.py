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

    async def __create_user_with_hash(self, user: UserInCreate) -> UserInCreate:
        password = await self.__password_service.hash(user.password)

        return UserInCreate(
            login=user.login,
            email=user.email,
            roles=user.roles,
            password=password,
        )

    async def create(self, user: UserInCreate) -> User:
        user_with_hash = await self.__create_user_with_hash(user)
        user = await self.__user_crud_service.create(data=user_with_hash)
        await self.__user_publisher.publish_model(user)
        return user
