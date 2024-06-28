from fastapi import APIRouter, Depends
from pydantic import UUID4
from pypika import Order

from src.domain.auth.dto.auth import JwtInResponse
from src.domain.common.data_models import JsonResponse
from src.domain.user.dto.user import (
    UserInCreate,
    UserInResponse,
    UserManyInRequest,
    UsersInResponse,
    UserInUpdate,
    UserInUpdateRequest,
    UserInLogin
)
from src.presentation.fastapi.depends.order import get_order
from src.presentation.fastapi.endpoints.user.controllers.create import CreateUserController
from src.presentation.fastapi.endpoints.user.controllers.delete import DeleteUserController
from src.presentation.fastapi.endpoints.user.controllers.login import LoginUserController
from src.presentation.fastapi.endpoints.user.controllers.read import ReadUserController
from src.presentation.fastapi.endpoints.user.controllers.read_by_course import ReadUserByCourseController
from src.presentation.fastapi.endpoints.user.controllers.read_many import ReadManyUserController
from src.presentation.fastapi.endpoints.user.controllers.update import UpdateUserController

user_api = APIRouter(prefix="/user", tags=["user"])


@user_api.post(
    "",
    response_model=JsonResponse[UserInResponse],
)
async def create(request: UserInCreate, controller: CreateUserController = Depends()) -> JsonResponse[UserInResponse]:
    return await controller(request)


@user_api.get(
    "/many",
    response_model=JsonResponse[UsersInResponse],
)
async def read_many(
    limit: int, offset: int, order: Order = Depends(get_order), controller: ReadManyUserController = Depends()
) -> JsonResponse[UsersInResponse]:
    request = UserManyInRequest(limit=limit, offset=offset, order=order)
    return await controller(request)


@user_api.get(
    "/course/{row_id}",
    response_model=JsonResponse[UsersInResponse],
)
async def read_by_course(
    row_id: UUID4, controller: ReadUserByCourseController = Depends()
) -> JsonResponse[UsersInResponse]:
    return await controller(row_id)


@user_api.get(
    "/{row_id}",
    response_model=JsonResponse[UserInResponse],
)
async def read_by_id(row_id: UUID4, controller: ReadUserController = Depends()) -> JsonResponse[UserInResponse]:
    return await controller(row_id)


@user_api.patch(
    "/{row_id}",
    response_model=JsonResponse[UserInResponse]
)
async def update(
    row_id: UUID4, request: UserInUpdateRequest, controller: UpdateUserController = Depends()
) -> JsonResponse[UserInResponse]:
    user_in_update = UserInUpdate(id=row_id, **request.model_dump())
    return await controller(user_in_update)


@user_api.delete(
    "/{row_id}",
    response_model=JsonResponse[UserInResponse],
)
async def delete(row_id: UUID4, controller: DeleteUserController = Depends()) -> JsonResponse[UserInResponse]:
    return await controller(row_id)


@user_api.post(
    "/login",
    response_model=JsonResponse[JwtInResponse]
)
async def login(request: UserInLogin, controller: LoginUserController = Depends()) -> JsonResponse[JwtInResponse]:
    return await controller(request)
