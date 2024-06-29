import os
from typing import AsyncIterator

import pytest
import pytest_asyncio
from httpx import AsyncClient
from pypika import PostgreSQLQuery, Table

import test
from src import AppContainer
from src.infrastructure.settings.stage.app import AppSettings
from src.infrastructure.settings.stage.base import AppEnvTypes
from src.presentation.fastapi.init.app import LmsApplicationFactory


@pytest_asyncio.fixture(scope="session", autouse=True)
def set_testing_env():
    os.environ["APP_ENV"] = AppEnvTypes.TEST.value


@pytest_asyncio.fixture(scope="session")
def app_container() -> AppContainer:
    container = AppContainer()
    container.wire(packages=[test])

    return container


@pytest_asyncio.fixture(scope="session")
def app_settings(app_container: AppContainer) -> AppSettings:
    return app_container.core.settings()


@pytest_asyncio.fixture(scope="session")
async def app_client() -> AsyncIterator[AsyncClient]:
    app = LmsApplicationFactory().create()
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest_asyncio.fixture(scope="session")
async def jwt_auth_header(app_container: AppContainer) -> dict:
    pass


async def insert_data(table_name, rows: list[tuple], app_container: AppContainer) -> None:
    table = Table(table_name)
    sql = PostgreSQLQuery.into(table).insert(*rows).get_sql()

    async with app_container.infrastructure.postgres_session_maker() as session:
        await session.execute(sql)
        await session.commit()
