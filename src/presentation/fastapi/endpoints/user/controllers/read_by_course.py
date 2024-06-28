from dependency_injector.wiring import Provide
from fastapi import Depends
from pydantic import UUID4

from src.application.service.user.crud import IUserCrudService
from src.domain.common.data_models import JsonResponse
from src.domain.user.dto.user import UserInResponse, UsersInResponse
from src.infrastructure.ioc.container.application import AppContainer
from src.presentation.fastapi.endpoints.controller_interface import IController


class ReadUserByCourseController(IController[UUID4, JsonResponse[UsersInResponse]]):

    def __init__(
        self,
        user_crud: IUserCrudService = Depends(Provide[AppContainer.services.user_crud_service])
    ):
        self.__user_crud = user_crud

    async def __call__(self, request: UUID4) -> JsonResponse[UsersInResponse]:
        users = await self.__user_crud.read_by_course_id(request)

        return JsonResponse[UsersInResponse](
            answer=UsersInResponse(
                rows=[UserInResponse.from_user(user) for user in users],
                count=len(users)
            )
        )
