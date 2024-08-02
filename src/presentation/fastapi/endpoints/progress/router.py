from fastapi import APIRouter, Depends
from pydantic import UUID4

from src.domain.common.data_models import JsonResponse, ManyInRequest, ManyJsonAnswer
from src.domain.common.enum.order import Order
from src.domain.progress.dto.progress import ProgressInResponse, ProgressInCreate
from src.domain.user.enum.roles import ALL_ROLES
from src.presentation.fastapi.depends.auth import has_roles
from src.presentation.fastapi.depends.order import get_order
from src.presentation.fastapi.endpoints.progress.controllers.create import CreateProgressController
from src.presentation.fastapi.endpoints.progress.controllers.read import ReadProgressController
from src.presentation.fastapi.endpoints.progress.controllers.read_many import ReadManyProgressController

progres_api = APIRouter(prefix="/progress", tags=["progress"], dependencies=[Depends(has_roles(ALL_ROLES))])


@progres_api.post(
    "",
    response_model=JsonResponse[ProgressInResponse],
)
async def create(
    request: ProgressInCreate, controller: CreateProgressController = Depends()
) -> JsonResponse[ProgressInResponse]:
    return await controller(request)


@progres_api.get(
    "/many",
    response_model=JsonResponse[ManyJsonAnswer[ProgressInResponse]],
)
async def read_many(
    limit: int, offset: int, order: Order = Depends(get_order), controller: ReadManyProgressController = Depends()
) -> JsonResponse[ManyJsonAnswer[ProgressInResponse]]:
    return await controller(
        ManyInRequest(
            limit=limit,
            offset=offset,
            order=order
        )
    )


@progres_api.get(
    "/{row_id}",
    response_model=JsonResponse[ProgressInResponse],
)
async def read_by_id(
    row_id: UUID4, controller: ReadProgressController = Depends()
) -> JsonResponse[ProgressInResponse]:
    return await controller(row_id)
