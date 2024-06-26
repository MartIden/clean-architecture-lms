from dependency_injector.wiring import Provide
from fastapi import Depends

from src.domain.common.data_models import JsonResponse
from src.domain.user.dto.user import UserInCreate, UserInResponse
from src.infrastructure.ioc.container.application import AppContainer
from src.infrastructure.persistence.postgres.repositiries.user import UserRepo
from src.presentation.fastapi.endpoints.controller_interface import IController


class CreateUserController(IController[UserInCreate, JsonResponse[UserInResponse]]):

    def __init__(
        self,
        repo: UserRepo = Depends(Provide[AppContainer.infrastructure.user_repo])
    ):
        self.__repo = repo

    async def __call__(self, request: UserInCreate) -> JsonResponse[UserInResponse]:
        user = await self.__repo.create(request)
        return JsonResponse(
            answer=UserInResponse.from_user(user)
        )
