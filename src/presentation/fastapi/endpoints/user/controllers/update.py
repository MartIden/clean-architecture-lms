from dependency_injector.wiring import Provide
from fastapi import Depends

from src.application.service.user.crud import IUserCrudService
from src.domain.common.data_models import JsonResponse
from src.domain.user.dto.user import UserInResponse, UserInUpdate
from src.domain.user.entity.user import User
from src.domain.user.enum.roles import ALL_ROLES
from src.domain.user.exception.user.update import UserUpdateError
from src.infrastructure.ioc.container.application import AppContainer
from src.presentation.fastapi.depends.auth import has_roles
from src.presentation.fastapi.endpoints.controller_interface import IController


class UpdateUserController(IController[UserInUpdate, JsonResponse[UserInResponse]]):

    def __init__(
        self,
        user_crud: IUserCrudService = Depends(Provide[AppContainer.services.user_crud_service]),
        current_user: User = Depends(has_roles(ALL_ROLES))
    ):
        self.__user_crud = user_crud
        self.__current_user = current_user

    async def __validate_current_user(self, request: UserInUpdate) -> None:
        user = await self.__user_crud.read_one(request.id)
        if self.__current_user.id != user.id:
            msg = "Допускается редактировать только свой профиль"
            raise UserUpdateError(msg)

    async def __call__(self, request: UserInUpdate) -> JsonResponse[UserInResponse]:
        await self.__validate_current_user(request)
        user = await self.__user_crud.update(request)

        return JsonResponse[UserInResponse](
            answer=UserInResponse.from_user(user)
        )
