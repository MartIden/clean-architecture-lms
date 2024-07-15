from fastapi import APIRouter, Depends
from pydantic import UUID4
from pypika import Order

from src.domain.common.data_models import (
    JsonResponse,
    ManyJsonAnswer,
    ManyInRequest
)
from src.domain.course.dto.course import (
    CourseInResponse,
    CourseByUserManyInRequest,
    CountCoursesInResponse
)
from src.domain.user.dto.user import (
    UserInResponse,
    UserInUpdate,
    UserInUpdateRequest,
)
from src.domain.user.enum.roles import ALL_ROLES
from src.presentation.fastapi.depends.auth import has_roles
from src.presentation.fastapi.depends.order import get_order
from src.presentation.fastapi.endpoints.user.controllers.count_by_user import CountByUserCourseController
from src.presentation.fastapi.endpoints.user.controllers.delete import DeleteUserController
from src.presentation.fastapi.endpoints.user.controllers.read import ReadUserController
from src.presentation.fastapi.endpoints.user.controllers.read_by_user import ReadByUserCourseController
from src.presentation.fastapi.endpoints.user.controllers.read_many import ReadManyUserController
from src.presentation.fastapi.endpoints.user.controllers.update import UpdateUserController

user_api = APIRouter(prefix="/user", tags=["user"], dependencies=[Depends(has_roles(ALL_ROLES))])


@user_api.get(
    "/many",
    response_model=JsonResponse[ManyJsonAnswer[UserInResponse]],
)
async def read_many(
    limit: int, offset: int, order: Order = Depends(get_order), controller: ReadManyUserController = Depends()
) -> JsonResponse[ManyJsonAnswer[UserInResponse]]:
    return await controller(
        ManyInRequest(
            limit=limit,
            offset=offset,
            order=order
        )
    )


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
    return await controller(
        UserInUpdate(
            id=row_id,
            **request.model_dump()
        )
    )


@user_api.delete(
    "/{row_id}",
    response_model=JsonResponse[UserInResponse],
)
async def delete(row_id: UUID4, controller: DeleteUserController = Depends()) -> JsonResponse[UserInResponse]:
    return await controller(row_id)


@user_api.get(
    "/{row_id}/course",
    response_model=JsonResponse[ManyJsonAnswer[CourseInResponse]],
)
async def read_courses_by_user(
    row_id: UUID4,
    limit: int,
    offset: int,
    order: Order = Depends(get_order),
    controller: ReadByUserCourseController = Depends()
) -> JsonResponse[ManyJsonAnswer[CourseInResponse]]:
    request = CourseByUserManyInRequest(
        id=row_id,
        limit=limit,
        offset=offset,
        order=order
    )
    return await controller(request)


@user_api.get(
    "/{row_id}/course/count",
    response_model=JsonResponse[CountCoursesInResponse],
)
async def count_courses_by_user(
    row_id: UUID4,
    controller: CountByUserCourseController = Depends()
) -> JsonResponse[CountCoursesInResponse]:
    return await controller(row_id)