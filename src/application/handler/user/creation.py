from abc import ABC, abstractmethod

from src.application.handler.interface import IHandler
from src.application.service.auth.password import IPasswordService
from src.application.service.user.crud import IUserCrudService
from src.domain.common.ports.publisher import IPublisher
from src.domain.user.dto.user import UserInCreate, UserInCreateEvent
from src.domain.user.entity.user import User


class IUserCreationHandler(IHandler):
    @abstractmethod
    async def __call__(self, event: UserInCreateEvent) -> User: ...


class UserCreationHandler(IUserCreationHandler):

    def __init__(
        self,
        password_service: IPasswordService,
        user_crud_service: IUserCrudService,
        user_publisher: IPublisher,
    ):
        self.__password_service = password_service
        self.__user_crud_service = user_crud_service
        self.__user_publisher = user_publisher

    async def __create_user_with_hash(self, event: UserInCreateEvent) -> UserInCreate:
        password = await self.__password_service.hash(event.password)

        return UserInCreate(
            login=event.login,
            email=event.email,
            roles=event.roles,
            password=password,
        )

    async def __call__(self, event: UserInCreateEvent) -> User:
        user_with_hash = await self.__create_user_with_hash(event)
        user = await self.__user_crud_service.create(data=user_with_hash)
        await self.__user_publisher.publish_model(user)
        return user
