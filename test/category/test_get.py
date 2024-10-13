import asyncio
import urllib.parse
from unittest.mock import AsyncMock, patch

from src.domain.category.dto.category import CategoryInCreate
from src.domain.user.value_object.email import UserEmail
from src.domain.user.value_object.login import UserLogin
from src.domain.user.value_object.password import UserPassword
from src.presentation.rmq.init.publisher import AbstractRmqPublisher
from src.presentation.rmq.publisher.user_new import UserNewPublisher
from test.conftest import *
from src.application.use_case.user.creation import IUserCreationCase
from src.domain.common.enum.order import Order
from src.domain.user.dto.user import UserInCreate


@pytest.mark.parametrize(
    ("category", "must_be"),
    [
        pytest.param(
            {
                "title": "1" * 20,
                "description": "1" * 20,
            },
            {
                "title": "1" * 20,
                "description": "1" * 20,
            }
        ),
    ]
)
@patch.object(UserNewPublisher, "publish_model", new_callable=AsyncMock)
@pytest.mark.asyncio(scope="session")
async def test_get(
    publish_model_mock: AsyncMock,
    category: dict,
    must_be: dict,
    app_client: AsyncClient,
    app_container: AppContainer
) -> None:
    await insert_data("categories", [], [], app_container)
    await insert_data("users", [], [], app_container)

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

    request = CategoryInCreate(**category)
    response = await app_client.post(f"/api/v1/category", json=request.model_dump(), headers=jwt_auth_header)

    assert response.status_code == 201
    created_category = response.json().get("answer", {})

    response = await app_client.get(f"/api/v1/category/{created_category.get('id')}", headers=jwt_auth_header)
    assert response.status_code == 200

    category = response.json().get("answer", {})

    assert created_category == category
