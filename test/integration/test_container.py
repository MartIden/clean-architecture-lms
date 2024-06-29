from conftest import *


@pytest.mark.parametrize(
    ("url",),
    [
        pytest.param(
            "/api/v1/course/7b8d3006-4db5-41c6-8910-110b3908d1ca"
        ),
        pytest.param(
            "/api/v1/course/7b8d3006-4db5-41c6-8910-110b3908d1ca"
        ),
    ]
)
@pytest.mark.asyncio
async def test_container(url: str, app_client: AsyncClient) -> None:
    response = await app_client.get(
        url,
        headers={"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImQ5ZWM3ZTA5LTc2NjItNDZkNy04NzQ3LThmNmVmNmU3NzdjOSIsImxvZ2luIjoicm9tYXNhNDY0IiwiZW1haWwiOiJyb21hc2E0NjRAZ21haWwuY29tIiwicm9sZXMiOlsiQURNSU4iXSwiZXhwIjoxNzIyMjM0NDE1LjcxNDYwNH0.gdNBAAa6xtY32_Db-FBlcq0fexg6pJoLXqANSvV2fLI"}
    )
    assert response.status_code == 200
