from dependency_injector.wiring import Provide
from fastapi import Depends
from pydantic import UUID4

from src.application.service.user.crud import IUserCrudService
from src.domain.common.data_models import JsonResponse
from src.domain.user.dto.user import UserInCreate, UserInResponse, UserManyInRequest, UsersInResponse
from src.infrastructure.ioc.container.application import AppContainer
from src.infrastructure.persistence.postgres.repositiries.user import UserRepo
from src.presentation.fastapi.endpoints.controller_interface import IController


class ReadManyUserController(IController[UserManyInRequest, JsonResponse[UsersInResponse]]):

    def __init__(
        self,
        user_crud: IUserCrudService = Depends(Provide[AppContainer.services.user_crud])
    ):
        self.__user_crud = user_crud

    async def __call__(self, request: UserManyInRequest) -> JsonResponse[UsersInResponse]:
        users = await self.__user_crud.read_many(
            limit=request.limit, offset=request.offset, order=request.order, order_by="created_at"
        )
        count = await self.__user_crud.count()
        return JsonResponse[UsersInResponse](
            answer=UsersInResponse(
                rows=[UserInResponse.from_user(user) for user in users],
                count=count
            )
        )
