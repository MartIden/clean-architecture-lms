import urllib.parse
from unittest.mock import AsyncMock

from src.presentation.rmq.init.publisher import AbstractRmqPublisher
from test.conftest import *
from src.application.use_case.user.creation import IUserCreationCase
from src.domain.common.enum.order import Order
from src.domain.user.dto.user import UserInCreate


@pytest.mark.parametrize(
    ("users", "limit", "offset", "order", "must_be"),
    [
        pytest.param(
            [
                {
                    "login": "1" * 20,
                    "email": f"{'1' * 20}@tt.tt",
                    "password": "password",
                    "roles": [UserRoleEnum.ADMIN]
                },
                {
                    "login": "2" * 20,
                    "email": f"{'2' * 20}@tt.tt",
                    "password": "password",
                    "roles": [UserRoleEnum.ADMIN]
                },
                {
                    "login": "3" * 20,
                    "email": f"{'3' * 20}@tt.tt",
                    "password": "password",
                    "roles": [UserRoleEnum.ADMIN]
                },
            ],
            10,
            0,
            Order.asc.value,
            [
                {
                    "login": "1" * 20,
                    "email": f"{'1' * 20}@tt.tt",
                    "password": "password",
                    "roles": [UserRoleEnum.ADMIN]
                },
                {
                    "login": "2" * 20,
                    "email": f"{'2' * 20}@tt.tt",
                    "password": "password",
                    "roles": [UserRoleEnum.ADMIN]
                },
                {
                    "login": "3" * 20,
                    "email": f"{'3' * 20}@tt.tt",
                    "password": "password",
                    "roles": [UserRoleEnum.ADMIN]
                },
            ],
        ),
    ]
)
@pytest.mark.asyncio(scope="session")
async def test_get_many_user(
    users: list[dict],
    limit: int,
    offset: int,
    order: Order,
    must_be: list[dict],
    app_client: AsyncClient,
    app_container: AppContainer
) -> None:
    await insert_data("users", [], [], app_container)

    with app_container.services.user_new_publisher.override(AsyncMock(spec=AbstractRmqPublisher)):
        user_creation_case: IUserCreationCase = app_container.services.user_creation_case()
        created_users = [await user_creation_case.create(UserInCreate(**user)) for user in users]

    jwt_auth_header = await create_jwt_auth_header(created_users[0], "password", app_container)

    params = {"limit": limit, "offset": offset, "order": order}
    url_params = urllib.parse.urlencode(params)

    response = await app_client.get(f"/api/v1/user/many?{url_params}", headers=jwt_auth_header)
    assert response.status_code == 200

    rows = response.json().get("answer", {}).get("rows")

    for i, row in enumerate(rows):
        assert must_be[i].get("login") == row.get("login")
        assert must_be[i].get("email") == row.get("email")
        assert must_be[i].get("roles") == row.get("roles")
