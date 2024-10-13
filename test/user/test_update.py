from unittest.mock import AsyncMock

from src.domain.user.value_object.email import UserEmail
from src.domain.user.value_object.login import UserLogin
from src.domain.user.value_object.password import UserPassword
from src.presentation.rmq.init.publisher import AbstractRmqPublisher
from test.conftest import *
from src.application.use_case.user.creation import IUserCreationCase
from src.domain.user.dto.user import UserInCreate, UserInUpdateRequest


@pytest.mark.asyncio(scope="session")
async def test_update_user(app_client: AsyncClient, app_container: AppContainer) -> None:
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

    request = UserInUpdateRequest(
        login="some_user_new",
        email=user.email,
        roles=user.roles
    )

    response = await app_client.patch(f"/api/v1/user/{user.id}", json=request.model_dump(), headers=jwt_auth_header)
    assert response.status_code == 200

    response_body = response.json().get("answer")

    assert response_body.get("login") == request.login
    assert response_body.get("email") == request.email
    assert response_body.get("roles") == request.roles
