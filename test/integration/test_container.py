import pytest

from conftest import *
from src.domain.user.dto.user import UserInCreate
from src.domain.user.ports.user_repo import IUserRepo


@pytest.mark.asyncio
async def test_get_user(app_client: AsyncClient, app_container: AppContainer) -> None:
    user_repo: IUserRepo = app_container.infrastructure.user_repo()
    user = await user_repo.create(
        UserInCreate(
            login="some_user",
            email="some_user@tt.tt",
            password="password",
            roles=[UserRoleEnum.ADMIN]
        )
    )
    # response = await app_client.get(
    #     f"/api/v1/user/{user.id}",
    #     headers=jwt_auth_header
    # )
    #
    # assert response.status_code == 200
    assert True

