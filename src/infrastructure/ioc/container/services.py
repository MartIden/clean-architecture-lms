from dependency_injector import containers, providers
from dependency_injector.providers import Factory

from src.application.service.auth.jwt import IJwtService
from src.application.service.auth.password import IPasswordService
from src.application.service.user.crud import IUserCrudService, UserCrudService
from src.application.use_case.auth.authorization import IAuthorizationCase, AuthorizationCase
from src.application.use_case.course.updater import ICourseUpdaterCase, CourseUpdaterCase
from src.application.use_case.user.creation import IUserCreationCase, UserCreationCase
from src.domain.common.ports.publisher import IPublisher
from src.infrastructure.ioc.container.core import CoreContainer
from src.infrastructure.ioc.container.infrastructure import InfrastructureContainer
from src.infrastructure.ioc.factory.jwt import JwtServiceFactory
from src.infrastructure.ioc.factory.password import PasswordServiceFactory
from src.presentation.rmq.publishers.user_new import UserNewPublisher


class ServicesContainer(containers.DeclarativeContainer):

    core: CoreContainer = providers.Container(CoreContainer)
    infrastructure: InfrastructureContainer = providers.Container(InfrastructureContainer)

    user_crud_service: Factory[IUserCrudService] = providers.Factory(UserCrudService, infrastructure.user_repo.provided)
    password_service: Factory[IPasswordService] = providers.Callable(PasswordServiceFactory.create)
    jwt_service: Factory[IJwtService] = providers.Callable(JwtServiceFactory(core.settings()).create)

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

    user_creation_case: Factory[IUserCreationCase] = providers.Factory(
        UserCreationCase,
        password_service.provided,
        user_crud_service.provided,
        user_new_publisher.provided,
    )

    course_updater_case: Factory[ICourseUpdaterCase] = providers.Factory(
        CourseUpdaterCase,
        infrastructure.course_repo
    )
