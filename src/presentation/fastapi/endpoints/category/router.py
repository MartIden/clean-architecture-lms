from fastapi import APIRouter, Depends
from pydantic import UUID4
from starlette import status
from starlette.responses import Response

from src.domain.category.dto.category import CategoryInResponse, CategoryInCreate, CategoryInUpdate, \
    CategoryInUpdateRequest
from src.domain.common.data_models import JsonResponse, ManyJsonAnswer, ManyInRequest
from src.domain.common.enum.order import Order
from src.domain.user.enum.roles import ALL_ROLES, UserRoleEnum
from src.presentation.fastapi.depends.auth import has_roles
from src.presentation.fastapi.depends.order import get_order
from src.presentation.fastapi.endpoints.category.controllers.create import CreateCategoryController
from src.presentation.fastapi.endpoints.category.controllers.delete import DeleteCategoryController
from src.presentation.fastapi.endpoints.category.controllers.read import ReadCategoryController
from src.presentation.fastapi.endpoints.category.controllers.read_many import ReadManyCategoryController
from src.presentation.fastapi.endpoints.category.controllers.update import UpdateCategoryController

category_api = APIRouter(prefix="/category", tags=["category"], dependencies=[Depends(has_roles(ALL_ROLES))])


@category_api.post(
    "",
    response_model=JsonResponse[CategoryInResponse],
    dependencies=[Depends(has_roles({UserRoleEnum.AUTHOR}))]
)
async def create(
    response: Response, request: CategoryInCreate, controller: CreateCategoryController = Depends()
) -> JsonResponse[CategoryInResponse]:
    response.status_code = status.HTTP_201_CREATED
    return await controller(request)


@category_api.get(
    "/many",
    response_model=JsonResponse[ManyJsonAnswer[CategoryInResponse]],
)
async def read_many(
    limit: int, offset: int, order: Order = Depends(get_order), controller: ReadManyCategoryController = Depends()
) -> JsonResponse[ManyJsonAnswer[CategoryInResponse]]:
    return await controller(
        ManyInRequest(
            limit=limit,
            offset=offset,
            order=order
        )
    )


@category_api.get(
    "/{row_id}",
    response_model=JsonResponse[CategoryInResponse],
)
async def read_one(
    row_id: UUID4,
    controller: ReadCategoryController = Depends()
) -> JsonResponse[CategoryInResponse]:
    return await controller(row_id)


@category_api.patch(
    "/{row_id}",
    response_model=JsonResponse[CategoryInResponse],
)
async def update(
    response: Response, row_id: UUID4, request: CategoryInUpdateRequest, controller: UpdateCategoryController = Depends()
) -> JsonResponse[CategoryInResponse]:
    to_update = CategoryInUpdate(id=row_id, **request.model_dump())
    response.status_code = status.HTTP_201_CREATED
    return await controller(to_update)


@category_api.delete(
    "/{row_id}",
    response_model=JsonResponse[CategoryInResponse],
)
async def delete(
    response: Response, row_id: UUID4, controller: DeleteCategoryController = Depends()
) -> JsonResponse[CategoryInResponse]:
    response.status_code = status.HTTP_201_CREATED
    return await controller(row_id)
