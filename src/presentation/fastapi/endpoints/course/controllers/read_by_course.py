from dependency_injector.wiring import Provide
from fastapi import Depends

from src.application.service.user.crud import IUserCrudService
from src.domain.common.data_models import JsonResponse, ManyJsonAnswer
from src.domain.user.dto.user import UserInResponse, UserByCourseManyInRequest
from src.infrastructure.ioc.container.application import AppContainer
from src.presentation.fastapi.endpoints.controller_interface import IController


class ReadUserByCourseController(
    IController[UserByCourseManyInRequest, JsonResponse[ManyJsonAnswer[UserInResponse]]]
):

    def __init__(
            self,
            user_crud: IUserCrudService = Depends(Provide[AppContainer.services.user_crud_service])
    ):
        self.__user_crud = user_crud

    async def __call__(self, request: UserByCourseManyInRequest) -> JsonResponse[ManyJsonAnswer[UserInResponse]]:
        users = await self.__user_crud.read_by_course_id(
            id_=request.id,
            limit=request.limit,
            offset=request.offset,
            order=request.order,
            order_by="created_at"
        )

        count = await self.__user_crud.count_by_course_id(request.id)

        return JsonResponse[ManyJsonAnswer[UserInResponse]](
            answer=ManyJsonAnswer[UserInResponse](
                rows=[UserInResponse.from_entity(user) for user in users],
                count=count
            )
        )