from fastapi import APIRouter, Depends
from pydantic import UUID4

from src.domain.common.data_models import JsonResponse
from src.domain.common.enum.order import Order
from src.domain.lesson.dto.lesson import (
    LessonInResponse,
    LessonInCreate,
    LessonsInResponse,
    LessonManyInRequest,
    LessonInUpdateRequest,
    LessonInUpdate
)
from src.presentation.fastapi.depends.order import get_order
from src.presentation.fastapi.endpoints.lesson.controllers.create import CreateLessonController
from src.presentation.fastapi.endpoints.lesson.controllers.delete import DeleteLessonController
from src.presentation.fastapi.endpoints.lesson.controllers.read import ReadLessonController
from src.presentation.fastapi.endpoints.lesson.controllers.read_by_course import ReadLessonsByCourseController
from src.presentation.fastapi.endpoints.lesson.controllers.read_many import ReadManyLessonController
from src.presentation.fastapi.endpoints.lesson.controllers.update import UpdateLessonController

lesson_api = APIRouter(prefix="/lesson", tags=["lesson"])


@lesson_api.post(
    "",
    response_model=JsonResponse[LessonInResponse],
)
async def create(
    request: LessonInCreate, controller: CreateLessonController = Depends()
) -> JsonResponse[LessonInResponse]:
    return await controller(request)


@lesson_api.get(
    "/many",
    response_model=JsonResponse[LessonsInResponse],
)
async def read_many(
    limit: int, offset: int, order: Order = Depends(get_order), controller: ReadManyLessonController = Depends()
) -> JsonResponse[LessonsInResponse]:
    request = LessonManyInRequest(limit=limit, offset=offset, order=order)
    return await controller(request)


@lesson_api.get(
    "/course/{row_id}",
    response_model=JsonResponse[LessonsInResponse],
)
async def read_by_course(
    row_id: UUID4, controller: ReadLessonsByCourseController = Depends()
) -> JsonResponse[LessonsInResponse]:
    return await controller(row_id)


@lesson_api.get(
    "/{row_id}",
    response_model=JsonResponse[LessonInResponse],
)
async def read(
    row_id: UUID4, controller: ReadLessonController = Depends()
) -> JsonResponse[LessonInResponse]:
    return await controller(row_id)


@lesson_api.patch(
    "/{row_id}",
    response_model=JsonResponse[LessonInResponse],
)
async def update(
    row_id: UUID4, request: LessonInUpdateRequest, controller: UpdateLessonController = Depends()
) -> JsonResponse[LessonInResponse]:
    to_update = LessonInUpdate(id=row_id, **request.model_dump())
    return await controller(to_update)


@lesson_api.delete(
    "/{row_id}",
    response_model=JsonResponse[LessonInResponse],
)
async def delete(
    row_id: UUID4, controller: DeleteLessonController = Depends()
) -> JsonResponse[LessonInResponse]:
    return await controller(row_id)