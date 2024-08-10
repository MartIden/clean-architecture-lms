from dependency_injector.wiring import Provide
from fastapi import Depends
from pydantic import UUID4

from src.application.service.user.crud import IUserCrudService
from src.domain.common.data_models import JsonResponse
from src.domain.user.dto.user import UsersCountInResponse
from src.infrastructure.ioc.container.application import AppContainer
from src.presentation.fastapi.endpoints.controller_interface import IController


class CountUserByCourseController(IController[UUID4, JsonResponse[UsersCountInResponse]]):

    def __init__(
        self,
        user_crud: IUserCrudService = Depends(Provide[AppContainer.services.user_crud_service])
    ):
        self.__user_crud = user_crud

    async def __call__(self, request: UUID4) -> JsonResponse[UsersCountInResponse]:
        count = await self.__user_crud.count_by_course_id(request)

        return JsonResponse[UsersCountInResponse](
            answer=UsersCountInResponse(
                count=count
            )
        )
