from dependency_injector.wiring import Provide
from fastapi import Depends

from src.application.service.user.crud import IUserCrudService
from src.domain.common.data_models import JsonResponse, ManyJsonAnswer, ManyInRequest
from src.domain.user.dto.user import UserInResponse
from src.infrastructure.ioc.container.application import AppContainer
from src.presentation.fastapi.endpoints.controller_interface import IController


class ReadManyUserController(IController[ManyInRequest, JsonResponse[ManyJsonAnswer[UserInResponse]]]):

    def __init__(
        self,
        user_crud: IUserCrudService = Depends(Provide[AppContainer.services.user_crud_service]),
    ):
        self.__user_crud = user_crud

    async def __call__(self, request: ManyInRequest) -> JsonResponse[ManyJsonAnswer[UserInResponse]]:
        users = await self.__user_crud.read_many(
            limit=request.limit, offset=request.offset, order=request.order, order_by="created_at"
        )
        count = await self.__user_crud.count()
        return JsonResponse[ManyJsonAnswer[UserInResponse]](
            answer=ManyJsonAnswer[UserInResponse](
                rows=[UserInResponse.from_user(user) for user in users],
                count=count
            )
        )
