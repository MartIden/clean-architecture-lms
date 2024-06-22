from dependency_injector import containers, providers
from dependency_injector.providers import Factory

from src.infrastructure.ioc.container.core import CoreContainer
from src.infrastructure.ioc.factory.postgres_connector import PostgresConnectorFactory, IPostgresConnectorFactory
from src.infrastructure.ioc.factory.rmq_connector import RmqConnectorFactory
from src.presentation.rmq.init.connector import IRmqConnector


class InfrastructureContainer(containers.DeclarativeContainer):
    core: CoreContainer = providers.Container(CoreContainer)

    rmq_connector: Factory[IRmqConnector] = providers.Singleton(
        RmqConnectorFactory(core.settings()).create
    )

    postgres_connector: Factory[IPostgresConnectorFactory] = providers.Singleton(
        PostgresConnectorFactory(core.settings()).create
    )

