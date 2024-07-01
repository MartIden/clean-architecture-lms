from dependency_injector import containers, providers
from dependency_injector.providers import Factory
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.domain.course.port.course_repo import ICourseRepo
from src.domain.course.port.user_course_repo import IUserCourseRepo
from src.domain.lesson.port.lesson_repo import ILessonRepo
from src.domain.user.ports.user_repo import IUserRepo
from src.infrastructure.ioc.container.core import CoreContainer
from src.infrastructure.ioc.factory.postgres_connector import PostgresConnectorFactory, IPostgresConnectorFactory
from src.infrastructure.ioc.factory.rmq_connector import RmqConnectorFactory
from src.infrastructure.persistence.postgres.repositiries.course import CourseRepo
from src.infrastructure.persistence.postgres.repositiries.lesson import LessonRepo
from src.infrastructure.persistence.postgres.repositiries.user import UserRepo
from src.infrastructure.persistence.postgres.repositiries.user_course import UserCourseRepo
from src.infrastructure.rmq.connector import IRmqConnector


class InfrastructureContainer(containers.DeclarativeContainer):
    core: CoreContainer = providers.Container(CoreContainer)

    rmq_connector: Factory[IRmqConnector] = providers.Singleton(
        RmqConnectorFactory(core.settings()).create
    )

    postgres_session_maker: Factory[async_sessionmaker[AsyncSession]] = providers.Callable(
        PostgresConnectorFactory(core.settings()).create
    )

    user_repo: Factory[IUserRepo] = providers.Factory(
        UserRepo,
        postgres_session_maker.provided
    )

    course_repo: Factory[ICourseRepo] = providers.Factory(
        CourseRepo,
        postgres_session_maker.provided
    )

    lesson_repo: Factory[ILessonRepo] = providers.Factory(
        LessonRepo,
        postgres_session_maker.provided
    )

    user_course_repo: Factory[IUserCourseRepo] = providers.Factory(
        UserCourseRepo,
        postgres_session_maker.provided
    )
