import os
import uuid
from datetime import datetime
from typing import AsyncIterator

import pytest_asyncio
from httpx import AsyncClient
from pypika import PostgreSQLQuery, Table
from pypika.queries import DropQueryBuilder
from sqlalchemy import text, create_engine
from alembic import command, config
from sqlalchemy.ext.asyncio import create_async_engine

import test
from src import AppContainer
from src.application.service.auth.password import IPasswordService
from src.application.use_case.auth.authorization import IAuthorizationCase
from src.domain.user.enum.roles import UserRoleEnum
from src.infrastructure.settings.stage.app import AppSettings
from src.infrastructure.settings.stage.base import AppEnvTypes
from src.presentation.fastapi.init.app import LmsApplicationFactory


@pytest_asyncio.fixture(scope="session", autouse=True)
async def init(app_container: AppContainer):
    os.environ["APP_ENV"] = AppEnvTypes.TEST.value
    settings: AppSettings = app_container.core.settings()

    await create_db(app_container)

    run_migrations("/Users/rdmorozkin/PycharmProjects/clean-architecture-lms/migration", settings.POSTGRES_URI)


def run_migrations(script_location: str, dsn: str) -> None:
    from alembic.config import Config
    from alembic import command

    alembic_cfg = Config()
    alembic_cfg.set_main_option('script_location', script_location)
    alembic_cfg.set_main_option('sqlalchemy.url', dsn)
    command.upgrade(alembic_cfg, 'head')


async def create_db(app_container: AppContainer):
    settings: AppSettings = app_container.core.settings()
    engine = create_async_engine(settings.POSTGRES_URI)

    try:
        async with engine.connect() as conn:
            await conn.execution_options(isolation_level="AUTOCOMMIT")
            await conn.execute(text("DROP DATABASE lms"))
    except Exception as e:
        pass
    #
    # async with engine.connect() as conn:
    #     await conn.execution_options(isolation_level="AUTOCOMMIT")
    #     await conn.execute(text("CREATE DATABASE lms"))


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
    now = int(datetime.now().timestamp())
    password_service: IPasswordService = app_container.services.password_service()
    password = password_service.hash("password")

    await insert_data(
        "users",
        ["id", "login", "password", "email", "roles", "created_at", "updated_at"],
        [(uuid.uuid4(), "user", password, "password@gmail.com", [UserRoleEnum.ADMIN], now, now)],
        app_container
    )

    auth_case: IAuthorizationCase = app_container.services.auth_case()
    token = await auth_case.authorize("user", "password")

    return {"Authorization": f"Bearer {token}"}


async def insert_data(table_name, columns: list[str], rows: list[tuple], app_container: AppContainer) -> None:
    table = Table(table_name)

    sql = PostgreSQLQuery.from_(table).delete().get_sql()
    session_maker = app_container.infrastructure.postgres_session_maker()

    async with session_maker() as session:
        await session.execute(text(sql))
        await session.commit()

    sql = PostgreSQLQuery.into(table).columns(*columns).insert(*rows).get_sql()

    async with session_maker() as session:
        await session.execute(text(sql))
        await session.commit()
