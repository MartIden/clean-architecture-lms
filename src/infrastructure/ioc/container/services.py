from dependency_injector import containers, providers
from dependency_injector.providers import Factory

from src.application.service.user.crud import IUserCrudService, UserCrudService
from src.infrastructure.ioc.container.core import CoreContainer
from src.infrastructure.ioc.container.infrastructure import InfrastructureContainer
from src.infrastructure.persistence.postgres.repositiries.user import UserRepo


class ServicesContainer(containers.DeclarativeContainer):
    core: CoreContainer = providers.Container(CoreContainer)
    infrastructure: InfrastructureContainer = providers.Container(InfrastructureContainer)

    user_crud: Factory[IUserCrudService] = providers.Factory(UserCrudService, infrastructure.user_repo.provided)
