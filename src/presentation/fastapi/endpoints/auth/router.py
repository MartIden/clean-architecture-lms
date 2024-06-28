from fastapi import APIRouter, Depends

from src.domain.auth.dto.auth import JwtInResponse
from src.domain.common.data_models import JsonResponse
from src.domain.user.dto.user import (
    UserInCreate,
    UserInResponse,
    UserInLogin
)
from src.presentation.fastapi.endpoints.auth.controllers.create import CreateUserController
from src.presentation.fastapi.endpoints.auth.controllers.login import LoginUserController

auth_api = APIRouter(tags=["auth"])


@auth_api.post(
    "/register",
    response_model=JsonResponse[UserInResponse],
)
async def register(request: UserInCreate, controller: CreateUserController = Depends()) -> JsonResponse[UserInResponse]:
    return await controller(request)

@auth_api.post(
    "/login",
    response_model=JsonResponse[JwtInResponse]
)
async def login(request: UserInLogin, controller: LoginUserController = Depends()) -> JsonResponse[JwtInResponse]:
    return await controller(request)
