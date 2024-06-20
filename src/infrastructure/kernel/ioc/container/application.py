from dependency_injector import containers, providers

from src import infrastructure, presentation
from src.infrastructure.kernel.ioc.container.core import CoreContainer
from src.infrastructure.kernel.ioc.container.infrastructure import InfrastructureContainer
from src.infrastructure.kernel.ioc.container.services import ServicesContainer


class ApplicationContainer(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(packages=[infrastructure, presentation])

    core: CoreContainer = providers.Container(CoreContainer)
    infrastructure: InfrastructureContainer = providers.Container(InfrastructureContainer)
    services: ServicesContainer = providers.Container(ServicesContainer)
