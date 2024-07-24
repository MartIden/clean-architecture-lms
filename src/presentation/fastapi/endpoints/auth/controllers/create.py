from dependency_injector.wiring import Provide
from fastapi import Depends

from src.application.use_case.user.creation import IUserCreationCase
from src.domain.common.data_models import JsonResponse
from src.domain.user.dto.user import UserInCreate, UserInResponse
from src.infrastructure.ioc.container.application import AppContainer
from src.presentation.fastapi.endpoints.controller_interface import IController


class CreateUserController(IController[UserInCreate, JsonResponse[UserInResponse]]):

    def __init__(
        self,
        user_creation_case: IUserCreationCase = Depends(Provide[AppContainer.services.user_creation_case])
    ):
        self.__user_creation_case = user_creation_case

    async def __call__(self, request: UserInCreate) -> JsonResponse[UserInResponse]:
        user = await self.__user_creation_case.create(request)
        return JsonResponse[UserInResponse](answer=UserInResponse.from_entity(user))
