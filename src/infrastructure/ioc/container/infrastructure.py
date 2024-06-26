from dependency_injector import containers, providers
from dependency_injector.providers import Factory
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.domain.user.ports.user_repo import IUserRepo
from src.infrastructure.ioc.container.core import CoreContainer
from src.infrastructure.ioc.factory.postgres_connector import PostgresConnectorFactory, IPostgresConnectorFactory
from src.infrastructure.ioc.factory.rmq_connector import RmqConnectorFactory
from src.infrastructure.persistence.postgres.repositiries.user import UserRepo
from src.infrastructure.rmq.connector import IRmqConnector


class InfrastructureContainer(containers.DeclarativeContainer):
    core: CoreContainer = providers.Container(CoreContainer)

    rmq_connector: Factory[IRmqConnector] = providers.Singleton(
        RmqConnectorFactory(core.settings()).create
    )

    postgres_session_maker: Factory[async_sessionmaker[AsyncSession]] = providers.Callable(
        PostgresConnectorFactory(core.settings()).create
    )

    user_repo: Factory[IUserRepo] = providers.Factory(UserRepo, postgres_session_maker.provided)
