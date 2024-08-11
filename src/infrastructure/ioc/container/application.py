from dependency_injector import containers, providers

from src.infrastructure.ioc.container.core import CoreContainer
from src.infrastructure.ioc.container.handler import HandlersContainer
from src.infrastructure.ioc.container.infrastructure import InfrastructureContainer
from src.infrastructure.ioc.container.service import ServicesContainer


class AppContainer(containers.DeclarativeContainer):
    core: CoreContainer = providers.Container(CoreContainer)
    infrastructure: InfrastructureContainer = providers.Container(InfrastructureContainer)
    services: ServicesContainer = providers.Container(ServicesContainer)
    handlers: HandlersContainer = providers.Container(HandlersContainer)
