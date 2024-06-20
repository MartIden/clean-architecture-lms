from dependency_injector import containers, providers

from src.infrastructure.kernel.ioc.container.core import CoreContainer
from src.infrastructure.kernel.ioc.container.infrastructure import InfrastructureContainer


class ServicesContainer(containers.DeclarativeContainer):
    core: CoreContainer = providers.Container(CoreContainer)
    infrastructure: InfrastructureContainer = providers.Container(InfrastructureContainer)
