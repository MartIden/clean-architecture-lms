from datetime import datetime

from pydantic import UUID4
from pypika import PostgreSQLQuery
from sqlalchemy import text

from src.domain.course.dto.course import CourseInCreate, CourseInUpdate
from src.domain.course.entity.course import Course
from src.domain.course.port.course_repo import ICourseRepo
from src.domain.user.entity.user import User
from src.infrastructure.persistence.postgres.repositiries.abstract import AbstractPostgresRepository


class CourseRepo(AbstractPostgresRepository[UUID4, User], ICourseRepo):
    _result_model = Course

    @property
    def table_name(self) -> str:
        return "courses"

    async def create(self, schema: CourseInCreate) -> User:
        now = int(datetime.now().timestamp())

        query = PostgreSQLQuery \
            .into(self.table) \
            .columns(
            self.table.title,
            self.table.description,
            self.table.cover,
            self.table.created_at,
            self.table.updated_at,
        ) \
            .insert(
            schema.title,
            schema.description,
            schema.cover,
            now,
            now,
        ) \
            .returning("*") \
            .get_sql()

        return await self._execute_one(text(query))

    async def update(self, schema: CourseInUpdate) -> User | None:
        course = await self.read_one(schema.id)

        if not course:
            return

        query = PostgreSQLQuery.update(self.table) \
            .set(self.table.title, schema.title or course.login) \
            .set(self.table.description, schema.description or course.email) \
            .set(self.table.cover, schema.cover or course.password) \
            .set(self.table.updated_at, int(datetime.now().timestamp())) \
            .where(self.table.id == schema.id) \
            .get_sql()

        await self.execute(text(query))
        return await self.read_one(schema.id)
