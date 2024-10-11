from unittest.mock import AsyncMock

from src.domain.user.value_object.email import UserEmail
from src.domain.user.value_object.login import UserLogin
from src.domain.user.value_object.password import UserPassword
from src.presentation.rmq.init.publisher import AbstractRmqPublisher
from test.conftest import *
from src.application.use_case.user.creation import IUserCreationCase
from src.domain.user.dto.user import UserInCreate


@pytest.mark.asyncio(scope="session")
async def test_get_user(app_client: AsyncClient, app_container: AppContainer) -> None:
    await insert_data("users", [], [], app_container)

    with app_container.services.user_new_publisher.override(AsyncMock(spec=AbstractRmqPublisher)):
        user_creation_case: IUserCreationCase = app_container.services.user_creation_case()
        user = await user_creation_case(
            UserInCreate(
                login=UserLogin("some_user"),
                email=UserEmail("some_user@tt.tt"),
                password=UserPassword("password"),
                roles=[UserRoleEnum.ADMIN]
            )
        )

    jwt_auth_header = await create_jwt_auth_header(user, "password", app_container)
    response = await app_client.get(f"/api/v1/user/{user.id}", headers=jwt_auth_header)
    assert response.status_code == 200

    response_body = response.json().get("answer")

    assert response_body.get("login") == user.login
    assert response_body.get("email") == user.email
    assert response_body.get("roles") == user.roles
