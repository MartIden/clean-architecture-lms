from dependency_injector import containers, providers
from dependency_injector.providers import Factory, Container

from src.application.handler.course.updater import CourseUpdaterHandler, ICourseUpdaterHandler
from src.application.handler.user.creation import IUserCreationHandler, UserCreationHandler
from src.domain.course.dto.course import CourseInUpdateEvent
from src.domain.user.dto.user import UserInCreateEvent
from src.infrastructure.ioc.container.core import CoreContainer
from src.infrastructure.ioc.container.infrastructure import InfrastructureContainer
from src.infrastructure.ioc.container.service import ServicesContainer
from src.infrastructure.ioc.factory.mediator import MediatorFactory, BindItem
from src.infrastructure.mediator.interface import IMediator


class HandlersContainer(containers.DeclarativeContainer):

    core: Container[CoreContainer] = providers.Container(CoreContainer)
    infrastructure: Container[InfrastructureContainer] = providers.Container(InfrastructureContainer)
    service: Container[ServicesContainer] = providers.Container(ServicesContainer)

    user_creation_handler: Factory[IUserCreationHandler] = providers.Factory(
        UserCreationHandler,
        service.password_service.provided,
        service.user_crud_service.provided,
        service.user_new_publisher.provided,
    )

    course_updater_handler: Factory[ICourseUpdaterHandler] = providers.Factory(
        CourseUpdaterHandler,
        infrastructure.course_repo
    )

    mediator: Factory[IMediator] = providers.Singleton(
        MediatorFactory(
            core.logger(),
            [
                BindItem(UserInCreateEvent, user_creation_handler()),
                BindItem(CourseInUpdateEvent, course_updater_handler()),
            ]
        ).create
    )
