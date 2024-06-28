from fastapi import APIRouter, Depends
from pydantic import UUID4

from src.domain.common.data_models import JsonResponse
from src.domain.common.enum.order import Order
from src.domain.course.dto.user_course import (
    UserCourseInResponse,
    UserCourseInCreate,
    UserCourseManyInRequest,
    UserCoursesInResponse,
    UserCourseInUpdateRequest,
    UserCourseInUpdate
)
from src.presentation.fastapi.depends.order import get_order
from src.presentation.fastapi.endpoints.user_course.controllers.create import CreateUserCourseController
from src.presentation.fastapi.endpoints.user_course.controllers.delete import DeleteUserCourseController
from src.presentation.fastapi.endpoints.user_course.controllers.read import ReadUserCourseController
from src.presentation.fastapi.endpoints.user_course.controllers.read_by_course import ReadByCourseUserCourseController
from src.presentation.fastapi.endpoints.user_course.controllers.read_by_user import ReadByUserUserCourseController
from src.presentation.fastapi.endpoints.user_course.controllers.read_many import ReadManyUserCourseController
from src.presentation.fastapi.endpoints.user_course.controllers.update import UpdateUserCourseController

user_course_api = APIRouter(prefix="/user-course", tags=["user_course"])

@user_course_api.post(
    "",
    response_model=JsonResponse[UserCourseInResponse],
)
async def create(
    request: UserCourseInCreate, controller: CreateUserCourseController = Depends()
) -> JsonResponse[UserCourseInResponse]:
    return await controller(request)


@user_course_api.get(
    "/many",
    response_model=JsonResponse[UserCoursesInResponse],
)
async def read_many(
    limit: int, offset: int, order: Order = Depends(get_order), controller: ReadManyUserCourseController = Depends()
) -> JsonResponse[UserCoursesInResponse]:
    request = UserCourseManyInRequest(limit=limit, offset=offset, order=order)
    return await controller(request)

@user_course_api.get(
    "/user/{row_id}",
    response_model=JsonResponse[UserCoursesInResponse],
)
async def read_by_user(
    row_id: UUID4, controller: ReadByUserUserCourseController = Depends()
) -> JsonResponse[UserCoursesInResponse]:
    return await controller(row_id)


@user_course_api.get(
    "/course/{row_id}",
    response_model=JsonResponse[UserCoursesInResponse],
)
async def read_by_course(
    row_id: UUID4, controller: ReadByCourseUserCourseController = Depends()
) -> JsonResponse[UserCoursesInResponse]:
    return await controller(row_id)


@user_course_api.get(
    "/{row_id}",
    response_model=JsonResponse[UserCourseInResponse],
)
async def read(
    row_id: UUID4, controller: ReadUserCourseController = Depends()
) -> JsonResponse[UserCourseInResponse]:
    return await controller(row_id)


@user_course_api.patch(
    "/{row_id}",
    response_model=JsonResponse[UserCourseInResponse],
)
async def update(
    row_id: UUID4, request: UserCourseInUpdateRequest, controller: UpdateUserCourseController = Depends()
) -> JsonResponse[UserCourseInResponse]:
    to_update = UserCourseInUpdate(id=row_id, **request.model_dump())
    return await controller(to_update)


@user_course_api.delete(
    "/{row_id}",
    response_model=JsonResponse[UserCourseInResponse],
)
async def delete(
    row_id: UUID4, controller: DeleteUserCourseController = Depends()
) -> JsonResponse[UserCourseInResponse]:
    return await controller(row_id)
