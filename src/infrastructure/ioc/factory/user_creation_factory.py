from typing import Callable

from src.application.use_case.user.creation import UserCreationCase
from src.application.service.auth.password import IPasswordService
from src.application.service.user.crud import IUserCrudService
from src.domain.common.ports.publisher import IPublisher


def create_user_creation_factory(
    password_service: IPasswordService,
    crud_service: IUserCrudService,
    user_publisher: IPublisher,
) -> Callable[[], UserCreationCase]:
    def create() -> UserCreationCase:
        return UserCreationCase(
            password_service,
            crud_service,
            user_publisher,
        )

    return create
