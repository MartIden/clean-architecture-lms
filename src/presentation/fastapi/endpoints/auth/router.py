from typing import Annotated

from dependency_injector.wiring import Provide
from fastapi import APIRouter, Depends
from starlette import status
from starlette.responses import Response

from src import AppContainer
from src.application.handler.user.creation import UserCreationHandler
from src.domain.auth.dto.auth import JwtInResponse
from src.domain.common.data_models import JsonResponse
from src.domain.user.dto.user import (
    UserInResponse,
    UserInLogin, UserCreateEvent
)
from src.infrastructure.mediator.mediator import IMediator
from src.presentation.fastapi.endpoints.auth.controllers.login import LoginUserController

auth_api = APIRouter(tags=["auth"])


@auth_api.post(
    "/register",
    response_model=JsonResponse[UserInResponse],
)
async def register(
    request: UserCreateEvent,
    response: Response,
    mediator: IMediator = Depends(Provide[AppContainer.handlers.mediator]),
) -> JsonResponse[UserInResponse]:
    response.status_code = status.HTTP_201_CREATED
    if results := await mediator.send(request):
        result = results.get(UserCreationHandler)
        return JsonResponse[UserInResponse](answer=UserInResponse.from_entity(result))


@auth_api.post(
    "/login",
    response_model=JsonResponse[JwtInResponse]
)
async def login(request: UserInLogin, controller: LoginUserController = Depends()) -> JsonResponse[JwtInResponse]:
    return await controller(request)
