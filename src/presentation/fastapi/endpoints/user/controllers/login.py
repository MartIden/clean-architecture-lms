from dependency_injector.wiring import Provide
from fastapi import Depends

from src.application.use_case.auth.authorization import IAuthorizationCase
from src.application.use_case.user.creation import IUserCreationCase
from src.domain.auth.dto.auth import JwtInResponse
from src.domain.common.data_models import JsonResponse
from src.domain.user.dto.user import UserInCreate, UserInResponse, UserInLogin
from src.infrastructure.ioc.container.application import AppContainer
from src.presentation.fastapi.endpoints.controller_interface import IController


class LoginUserController(IController[UserInLogin, JsonResponse[JwtInResponse]]):

    def __init__(
        self,
        auth_case: IAuthorizationCase = Depends(Provide[AppContainer.services.auth_case])
    ):
        self.__auth_case = auth_case

    async def __call__(self, request: UserInLogin) -> JsonResponse[JwtInResponse]:
        token = await self.__auth_case.authorize(request.login, request.password)
        return JsonResponse[JwtInResponse](answer=JwtInResponse(
            token=token,
            token_type="bearer"
        ))
