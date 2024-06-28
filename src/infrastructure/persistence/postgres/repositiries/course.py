from datetime import datetime
from typing import Sequence

from pydantic import UUID4
from pypika import PostgreSQLQuery, Table, JoinType, functions
from sqlalchemy import text

from src.domain.common.enum.order import Order
from src.domain.course.dto.course import CourseInCreate, CourseInUpdate
from src.domain.course.entity.course import Course
from src.domain.course.port.course_repo import ICourseRepo
from src.infrastructure.persistence.postgres.repositiries.abstract import AbstractPostgresRepository


class CourseRepo(AbstractPostgresRepository[UUID4, Course], ICourseRepo):

    _result_model = Course

    @property
    def table_name(self) -> str:
        return "courses"

    async def create(self, schema: CourseInCreate) -> Course:
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

    async def update(self, schema: CourseInUpdate) -> Course | None:
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

    async def read_by_user_id(self, id_: UUID4, limit: int, offset: int, order: Order, order_by: str) -> Sequence[Course]:
        users_courses_table = Table("users_courses")
        users_table = Table("users")

        sql = (
            self.from_table.select(
                self.table.id,
                self.table.title,
                self.table.description,
                self.table.cover,
                self.table.updated_at,
                self.table.created_at,
            )
            .join(users_courses_table, JoinType.left)
            .on(self.table.id == users_courses_table.course_id)
            .join(users_table, JoinType.left)
            .on(users_table.id == users_courses_table.user_id)
            .where(users_table.id == id_)
            .orderby(order_by, order=order)[offset:limit]
            .get_sql()
        )

        return await self._execute_many(text(sql))

    async def count_by_user_id(self, id_: UUID4) -> int:
        users_courses_table, users_table = Table("users_courses"), Table("users")

        sql = (
            self.from_table.select(functions.Count("*"))
            .join(users_courses_table, JoinType.left)
            .on(self.table.id == users_courses_table.course_id)
            .join(users_table, JoinType.left)
            .on(users_table.id == users_courses_table.user_id)
            .where(users_table.id == id_).get_sql()
        )

        rows = await self.execute_with_return(text(sql))
        return self._get_counter(rows)
