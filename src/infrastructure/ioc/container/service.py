from dependency_injector import containers, providers
from dependency_injector.providers import Factory, Container, Callable

from src.application.service.auth.jwt import IJwtService
from src.application.service.auth.password import IPasswordService
from src.application.service.user.crud import IUserCrudService, UserCrudService
from src.application.service.auth.authorization import IAuthorizationCase, AuthorizationCase
from src.application.handler.course.updater import ICourseUpdaterCase, CourseUpdaterCase
from src.application.handler.progress.adder import IProgressAdderCase, ProgressAdderCase
from src.application.handler.progress.by_course_getter import (
    IByCourseProgressGetterUseCase,
    ByCourseProgressGetterUseCase
)
from src.domain.common.ports.publisher import IPublisher
from src.infrastructure.ioc.container.core import CoreContainer
from src.infrastructure.ioc.container.infrastructure import InfrastructureContainer
from src.infrastructure.ioc.factory.jwt import JwtServiceFactory
from src.infrastructure.ioc.factory.password import PasswordServiceFactory
from src.presentation.rmq.publisher.user_new import UserNewPublisher


class ServicesContainer(containers.DeclarativeContainer):

    core: Container[CoreContainer] = providers.Container(CoreContainer)
    infrastructure: Container[InfrastructureContainer] = providers.Container(InfrastructureContainer)

    user_crud_service: Factory[IUserCrudService] = providers.Factory(
        UserCrudService,
        infrastructure.user_repo.provided
    )

    password_service: Callable[Factory[IPasswordService]] = providers.Callable(
        PasswordServiceFactory(core.settings()).create

    )

    jwt_service: Factory[IJwtService] = providers.Callable(
        JwtServiceFactory(core.settings()).create
    )

    auth_case: Factory[IAuthorizationCase] = providers.Factory(
        AuthorizationCase,
        user_crud_service.provided,
        password_service.provided,
        jwt_service.provided
    )

    user_new_publisher: Factory[IPublisher] = providers.Factory(
        UserNewPublisher,
        infrastructure.rmq_connector.provided,
        core.settings.provided,
        core.logger.provided,
    )

    course_updater_case: Factory[ICourseUpdaterCase] = providers.Factory(
        CourseUpdaterCase,
        infrastructure.course_repo
    )

    progress_adder_case: Factory[IProgressAdderCase] = providers.Factory(
        ProgressAdderCase,
        infrastructure.lesson_repo,
        infrastructure.progress_repo,
    )

    by_course_progress_getter_case: Factory[IByCourseProgressGetterUseCase] = providers.Factory(
        ByCourseProgressGetterUseCase,
        infrastructure.progress_repo,
        infrastructure.lesson_repo,
    )
