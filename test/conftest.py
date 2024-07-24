import asyncio
import os
import random
import uuid
from asyncio import AbstractEventLoop
from datetime import datetime
from typing import AsyncIterator, Generator

import nest_asyncio
import pytest
import pytest_asyncio
from httpx import AsyncClient
from pypika import PostgreSQLQuery, Table
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from src import AppContainer
from src.application.service.auth.password import IPasswordService
from src.application.use_case.auth.authorization import IAuthorizationCase
from src.domain.user.entity.user import User
from src.domain.user.enum.roles import UserRoleEnum
from src.infrastructure.settings.stage.app import AppSettings
from src.infrastructure.settings.stage.base import AppEnvTypes
from src.presentation.fastapi.init.app import LmsApplicationFactory


@pytest.fixture(autouse=True, scope="session")
async def init(app_container: AppContainer):
    os.environ["APP_ENV"] = AppEnvTypes.TEST.value
    await reset_db(app_container)
    settings: AppSettings = app_container.core.settings()
    run_migrations(f"{settings.ROOT_DIR}/migration", settings.POSTGRES_URI)


def run_migrations(script_location: str, dsn: str) -> None:
    from alembic.config import Config
    from alembic import command

    alembic_cfg = Config()
    alembic_cfg.set_main_option('script_location', script_location)
    alembic_cfg.set_main_option('sqlalchemy.url', dsn)
    command.upgrade(alembic_cfg, 'head')


async def reset_db(app_container: AppContainer) -> None:
    settings: AppSettings = app_container.core.settings()
    engine = create_async_engine(settings.POSTGRES_URI)

    new_db_name = f"test_database"

    try:
        async with engine.connect() as conn:
            await conn.execution_options(isolation_level="AUTOCOMMIT")
            await conn.execute(text(f"DROP DATABASE {new_db_name} WITH (FORCE)"))
    except Exception:
        return

    async with engine.connect() as conn:
        await conn.execution_options(isolation_level="AUTOCOMMIT")
        await conn.execute(text(f"CREATE DATABASE {new_db_name}"))

    os.environ["POSTGRES_URI"] = settings.POSTGRES_URI + new_db_name


@pytest.fixture(scope="session")
def app_container() -> AppContainer:
    return AppContainer()


@pytest.fixture(scope="session")
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
    login = str(random.randint(1, 10_000))

    await insert_data(
        "users",
        ["id", "login", "password", "email", "roles", "created_at", "updated_at"],
        [(uuid.uuid4(), login, password, f"{login}@tt.tt", [UserRoleEnum.ADMIN], now, now)],
        app_container
    )

    auth_case: IAuthorizationCase = app_container.services.auth_case()
    token = await auth_case.authorize(login, "password")

    return {"Authorization": f"Bearer {token}"}


async def create_jwt_auth_header(user: User, raw_password: str, app_container: AppContainer) -> dict:
    auth_case: IAuthorizationCase = app_container.services.auth_case()
    token = await auth_case.authorize(user.login, raw_password)
    return {"Authorization": f"Bearer {token}"}


async def insert_data(table_name, columns: list[str], rows: list[tuple], app_container: AppContainer) -> None:
    table = Table(table_name)

    sql = PostgreSQLQuery.from_(table).delete().get_sql()
    session_maker = app_container.infrastructure.postgres_session_manager()

    async with session_maker.session() as session:
        await session.execute(text(sql))
        await session.commit()

    if not rows:
        return

    sql = PostgreSQLQuery.into(table).columns(*columns).insert(*rows).get_sql()

    async with session_maker.session() as session:
        await session.execute(text(sql))
        await session.commit()


@pytest.fixture(autouse=True, scope="session")
def event_loop():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()
