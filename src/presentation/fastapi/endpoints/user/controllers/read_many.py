from dependency_injector.wiring import Provide
from fastapi import Depends
from pydantic import UUID4

from src.domain.common.data_models import JsonResponse
from src.domain.user.dto.user import UserInCreate, UserInResponse, UserManyInRequest, UsersInResponse
from src.infrastructure.ioc.container.application import AppContainer
from src.infrastructure.persistence.postgres.repositiries.user import UserRepo
from src.presentation.fastapi.endpoints.controller_interface import IController


class ReadManyUserController(IController[UserManyInRequest, JsonResponse[UsersInResponse]]):

    def __init__(
        self,
        repo: UserRepo = Depends(Provide[AppContainer.infrastructure.user_repo])
    ):
        self.__repo = repo

    async def __call__(self, request: UserManyInRequest) -> JsonResponse[UsersInResponse]:
        users = await self.__repo.read_many(limit=request.limit, offset=request.offset, order=request.order)
        count = await self.__repo.count()
        return JsonResponse[UsersInResponse](
            answer=UsersInResponse(
                rows=[UserInResponse.from_user(user) for user in users],
                count=count
            )
        )
