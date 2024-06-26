from dependency_injector import containers, providers
from dependency_injector.providers import Factory

from src.infrastructure.ioc.container.core import CoreContainer
from src.infrastructure.ioc.container.infrastructure import InfrastructureContainer
from src.infrastructure.persistence.postgres.repositiries.user import UserRepo


class ServicesContainer(containers.DeclarativeContainer):
    core: CoreContainer = providers.Container(CoreContainer)
    infrastructure: InfrastructureContainer = providers.Container(InfrastructureContainer)
    # user_repo: Factory[UserRepo] = providers.Factory(UserRepo, infrastructure.postgres_connector())
