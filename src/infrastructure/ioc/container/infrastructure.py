from dependency_injector import containers, providers
from dependency_injector.providers import Factory
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine, AsyncEngine

from src.domain.course.port.course_repo import ICourseRepo
from src.domain.course.port.user_course_repo import IUserCourseRepo
from src.domain.lesson.port.lesson_repo import ILessonRepo
from src.domain.user.ports.user_repo import IUserRepo
from src.infrastructure.ioc.container.core import CoreContainer
from src.infrastructure.ioc.factory.postgres_connector import SessionManager
from src.infrastructure.ioc.factory.rmq_connector import RmqConnectorFactory
from src.infrastructure.persistence.postgres.repositiries.course import CourseRepo
from src.infrastructure.persistence.postgres.repositiries.lesson import LessonRepo
from src.infrastructure.persistence.postgres.repositiries.user import UserRepo
from src.infrastructure.persistence.postgres.repositiries.user_course import UserCourseRepo
from src.infrastructure.rmq.connector import IRmqConnector


class InfrastructureContainer(containers.DeclarativeContainer):
    core: CoreContainer = providers.Container(CoreContainer)

    rmq_connector: Factory[IRmqConnector] = providers.Factory(
        RmqConnectorFactory(core.settings()).create
    )

    engine: Factory[AsyncEngine] = providers.Singleton(
        create_async_engine,
        url=core.settings.provided.POSTGRES_URI,
    )

    async_session_factory: Factory[async_sessionmaker[AsyncSession]] = providers.Singleton(
        async_sessionmaker,
        bind=engine.provided,
        autoflush=True,
        expire_on_commit=False,
        class_=AsyncSession
    )

    postgres_session_manager: Factory[SessionManager] = providers.Singleton(
        SessionManager, async_session_factory.provided
    )

    user_repo: Factory[IUserRepo] = providers.Factory(
        UserRepo,
        async_session_factory.provided
    )

    course_repo: Factory[ICourseRepo] = providers.Factory(
        CourseRepo,
        async_session_factory.provided
    )

    lesson_repo: Factory[ILessonRepo] = providers.Factory(
        LessonRepo,
        async_session_factory.provided
    )

    user_course_repo: Factory[IUserCourseRepo] = providers.Factory(
        UserCourseRepo,
        async_session_factory.provided
    )
