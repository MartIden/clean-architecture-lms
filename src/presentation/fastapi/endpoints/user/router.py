from fastapi import APIRouter, Depends

from src.domain.common.data_models import JsonResponse
from src.domain.user.dto.user import UserInCreate, UserInResponse
from src.presentation.fastapi.endpoints.user.controllers.create import CreateUserController

user_api = APIRouter(prefix="/user")


@user_api.post(
    "",
    response_model=JsonResponse[UserInResponse],
)
async def create(request: UserInCreate, controller: CreateUserController = Depends()) -> JsonResponse[UserInResponse]:
    return await controller(request)
