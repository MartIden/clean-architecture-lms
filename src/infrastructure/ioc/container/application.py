from dependency_injector import containers, providers

from src.infrastructure.ioc.container.core import CoreContainer
from src.infrastructure.ioc.container.infrastructure import InfrastructureContainer
from src.infrastructure.ioc.container.services import ServicesContainer


class AppContainer(containers.DeclarativeContainer):
    core: CoreContainer = providers.Container(CoreContainer)
    infrastructure: InfrastructureContainer = providers.Container(InfrastructureContainer)
    services: ServicesContainer = providers.Container(ServicesContainer)
