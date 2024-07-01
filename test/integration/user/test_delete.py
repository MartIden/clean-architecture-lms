import pytest

from test.conftest import *
from src.application.use_case.user.creation import IUserCreationCase
from src.domain.user.dto.user import UserInCreate


@pytest.mark.asyncio
async def test_delete_user(app_client: AsyncClient, app_container: AppContainer) -> None:
    await insert_data("users", [], [], app_container)

    user_creation_case: IUserCreationCase = app_container.services.user_creation_case()

    user = await user_creation_case.create(
        UserInCreate(
            login="some_user",
            email="some_user@tt.tt",
            password="password",
            roles=[UserRoleEnum.ADMIN]
        )
    )

    jwt_auth_header = await create_jwt_auth_header(user, "password", app_container)
    response = await app_client.delete(f"/api/v1/user/{user.id}", headers=jwt_auth_header)
    assert response.status_code == 200

    response_body = response.json().get("answer")

    assert response_body.get("login") == user.login
    assert response_body.get("email") == user.email
    assert response_body.get("roles") == user.roles
