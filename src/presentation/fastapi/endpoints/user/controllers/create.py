from dependency_injector.wiring import Provide
from fastapi import Depends

from src.application.service.user.crud import IUserCrudService
from src.domain.common.data_models import JsonResponse
from src.domain.user.dto.user import UserInCreate, UserInResponse
from src.infrastructure.ioc.container.application import AppContainer
from src.infrastructure.persistence.postgres.repositiries.user import UserRepo
from src.presentation.fastapi.endpoints.controller_interface import IController


class CreateUserController(IController[UserInCreate, JsonResponse[UserInResponse]]):

    def __init__(
        self,
        user_crud: IUserCrudService = Depends(Provide[AppContainer.services.user_crud])
    ):
        self.__user_crud = user_crud

    async def __call__(self, request: UserInCreate) -> JsonResponse[UserInResponse]:
        user = await self.__user_crud.create(request)
        return JsonResponse[UserInResponse](
            answer=UserInResponse.from_user(user)
        )
