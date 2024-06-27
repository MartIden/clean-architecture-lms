from dependency_injector.wiring import Provide
from fastapi import Depends

from src.application.service.user.crud import IUserCrudService
from src.domain.common.data_models import JsonResponse
from src.domain.user.dto.user import UserInCreate, UserInResponse, UserInUpdate
from src.infrastructure.ioc.container.application import AppContainer
from src.infrastructure.persistence.postgres.repositiries.user import UserRepo
from src.presentation.fastapi.endpoints.controller_interface import IController


class UpdateUserController(IController[UserInUpdate, JsonResponse[UserInResponse]]):

    def __init__(
        self,
        user_crud: IUserCrudService = Depends(Provide[AppContainer.services.user_crud_service])
    ):
        self.__user_crud = user_crud

    async def __call__(self, request: UserInUpdate) -> JsonResponse[UserInResponse]:
        user = await self.__user_crud.update(request)
        return JsonResponse[UserInResponse](
            answer=UserInResponse.from_user(user)
        )
