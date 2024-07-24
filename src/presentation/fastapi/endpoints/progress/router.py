from fastapi import APIRouter, Depends

from src.domain.common.data_models import JsonResponse
from src.domain.progress.dto.progress import ProgressInResponse, ProgressInCreate
from src.domain.user.enum.roles import ALL_ROLES
from src.presentation.fastapi.depends.auth import has_roles
from src.presentation.fastapi.endpoints.progress.controllers.create import CreateProgressController

progres_api = APIRouter(prefix="/progress", tags=["progress"], dependencies=[Depends(has_roles(ALL_ROLES))])


@progres_api.post(
    "",
    response_model=JsonResponse[ProgressInResponse],
)
async def create(
    request: ProgressInCreate, controller: CreateProgressController = Depends()
) -> JsonResponse[ProgressInResponse]:
    return await controller(request)
