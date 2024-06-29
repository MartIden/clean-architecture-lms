from fastapi import APIRouter, Depends
from pydantic import UUID4

from src.domain.common.data_models import JsonResponse
from src.domain.common.enum.order import Order
from src.domain.course.dto.course import (
    CourseInCreate,
    CourseInResponse,
    CoursesInResponse,
    CourseManyInRequest,
    CourseInUpdateRequest,
    CourseInUpdate,
    CourseByUserManyInRequest
)
from src.domain.user.enum.roles import ALL_ROLES, UserRoleEnum
from src.presentation.fastapi.depends.auth import has_roles
from src.presentation.fastapi.depends.order import get_order
from src.presentation.fastapi.endpoints.course.controllers.create import CreateCourseController
from src.presentation.fastapi.endpoints.course.controllers.delete import DeleteCourseController
from src.presentation.fastapi.endpoints.course.controllers.read import ReadCourseController
from src.presentation.fastapi.endpoints.course.controllers.read_by_user import ReadByUserCourseController
from src.presentation.fastapi.endpoints.course.controllers.read_many import ReadManyCourseController
from src.presentation.fastapi.endpoints.course.controllers.update import UpdateCourseController

course_api = APIRouter(prefix="/course", tags=["course"], dependencies=[Depends(has_roles(ALL_ROLES))])


@course_api.post(
    "",
    response_model=JsonResponse[CourseInResponse],
    dependencies=[Depends(has_roles([UserRoleEnum.AUTHOR]))]
)
async def create(
    request: CourseInCreate, controller: CreateCourseController = Depends()
) -> JsonResponse[CourseInResponse]:
    return await controller(request)


@course_api.get(
    "/many",
    response_model=JsonResponse[CoursesInResponse],
)
async def read_many(
    limit: int, offset: int, order: Order = Depends(get_order), controller: ReadManyCourseController = Depends()
) -> JsonResponse[CoursesInResponse]:
    request = CourseManyInRequest(limit=limit, offset=offset, order=order)
    return await controller(request)


@course_api.get(
    "/user/{row_id}",
    response_model=JsonResponse[CoursesInResponse],
)
async def read_by_user(
    row_id: UUID4,
    limit: int,
    offset: int,
    order: Order = Depends(get_order),
    controller: ReadByUserCourseController = Depends()
) -> JsonResponse[CoursesInResponse]:
    request = CourseByUserManyInRequest(
        id=row_id,
        limit=limit,
        offset=offset,
        order=order
    )
    return await controller(request)


@course_api.get(
    "/{row_id}",
    response_model=JsonResponse[CourseInResponse],
)
async def read(
    row_id: UUID4, controller: ReadCourseController = Depends()
) -> JsonResponse[CourseInResponse]:
    return await controller(row_id)


@course_api.patch(
    "/{row_id}",
    response_model=JsonResponse[CourseInResponse],
    dependencies=[Depends(has_roles([UserRoleEnum.AUTHOR]))]
)
async def update(
    row_id: UUID4, request: CourseInUpdateRequest, controller: UpdateCourseController = Depends()
) -> JsonResponse[CourseInResponse]:
    to_update = CourseInUpdate(id=row_id, **request.model_dump())
    return await controller(to_update)


@course_api.delete(
    "/{row_id}",
    response_model=JsonResponse[CourseInResponse],
)
async def delete(
    row_id: UUID4, controller: DeleteCourseController = Depends()
) -> JsonResponse[CourseInResponse]:
    return await controller(row_id)
