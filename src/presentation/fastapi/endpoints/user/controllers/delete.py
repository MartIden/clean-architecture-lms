from dependency_injector.wiring import Provide
from fastapi import Depends
from pydantic import UUID4

from src.application.service.user.crud import IUserCrudService
from src.domain.common.data_models import JsonResponse
from src.domain.user.dto.user import UserInResponse
from src.domain.user.entity.user import User
from src.domain.user.enum.roles import ALL_ROLES
from src.domain.user.exception.user.delete import UserDeleteError
from src.infrastructure.ioc.container.application import AppContainer
from src.presentation.fastapi.depends.auth import has_roles
from src.presentation.fastapi.endpoints.controller_interface import IController


class DeleteUserController(IController[UUID4, JsonResponse[UserInResponse]]):

    def __init__(
        self,
        user_crud: IUserCrudService = Depends(Provide[AppContainer.services.user_crud_service]),
        current_user: User = Depends(has_roles(ALL_ROLES))
    ):
        self.__user_crud = user_crud
        self.__current_user = current_user

    async def __call__(self, id_: UUID4) -> JsonResponse[UserInResponse]:
        user = await self.__user_crud.read_one(id_)

        if user.id != self.__current_user.id:
            raise UserDeleteError("Допускается удалять только свой профиль")

        user = await self.__user_crud.delete(id_)

        return JsonResponse[UserInResponse](
            answer=UserInResponse.from_entity(user)
        )
