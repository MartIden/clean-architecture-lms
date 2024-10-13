from unittest.mock import patch, AsyncMock

from src.domain.user.value_object.email import UserEmail
from src.domain.user.value_object.login import UserLogin
from src.domain.user.value_object.password import UserPassword
from src.presentation.rmq.publisher.user_new import UserNewPublisher
from test.conftest import *
from src.domain.user.dto.user import UserInCreate
from src.domain.user.enum.roles import UserRoleEnum


@patch.object(UserNewPublisher, "publish_model", new_callable=AsyncMock)
@pytest.mark.asyncio(scope="session")
async def test_create(publish_model_mock, app_client: AsyncClient, app_container: AppContainer) -> None:
    await insert_data("users", [], [], app_container)

    request = UserInCreate(
        login=UserLogin("some_user"),
        email=UserEmail("some_user@tt.tt"),
        password=UserPassword("password"),
        roles=[UserRoleEnum.ADMIN]
    )

    response = await app_client.post(f"/api/v1/register", json=request.model_dump())
    assert response.status_code == 201

    response_body = response.json().get("answer")

    assert response_body.get("login") == request.login
    assert response_body.get("email") == request.email
    assert response_body.get("roles") == request.roles
    assert publish_model_mock.call_count == 1
