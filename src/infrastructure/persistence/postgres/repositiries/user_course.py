from datetime import datetime
from typing import Sequence

from pydantic import UUID4
from pypika import PostgreSQLQuery, functions
from sqlalchemy import text

from src.domain.course.dto.user_course import UserCourseInUpdate, UserCourseInCreate
from src.domain.course.entity.user_course import UserCourse
from src.domain.course.port.user_course_repo import IUserCourseRepo
from src.infrastructure.persistence.postgres.repositiries.abstract import AbstractPostgresRepository


class UserCourseRepo(
    AbstractPostgresRepository[
        UUID4,
        UserCourseInCreate,
        UserCourseInUpdate,
        UserCourse
    ],
    IUserCourseRepo
):

    _result_model = UserCourse

    @property
    def table_name(self) -> str:
        return "users_courses"

    async def create(self, schema: UserCourseInCreate) -> UserCourse:
        now = int(datetime.now().timestamp())

        query = PostgreSQLQuery \
            .into(self.table) \
            .columns(
                self.table.user_id,
                self.table.course_id,
                self.table.created_at,
                self.table.updated_at,
            ) \
            .insert(
                schema.user_id,
                schema.course_id,
                now,
                now,
            ) \
            .returning("*") \
            .get_sql()

        return await self._execute_one(text(query))

    async def update(self, schema: UserCourseInUpdate) -> UserCourse | None:
        user_course = await self.read_one(schema.id)

        if not user_course:
            return

        query = PostgreSQLQuery.update(self.table) \
            .set(self.table.user_id, schema.user_id or user_course.user_id) \
            .set(self.table.course_id, schema.course_id or user_course.course_id) \
            .set(self.table.password, schema.password or user_course.password) \
            .set(self.table.updated_at, int(datetime.now().timestamp())) \
            .where(self.table.id == schema.id) \
            .get_sql()

        await self.execute(text(query))
        return await self.read_one(schema.id)

    async def read_by_user_id(self, id_: UUID4) -> Sequence[UserCourse]:
        sql = self.from_table.select('*').where(self.table.user_id == id_).get_sql()
        return await self._execute_many(text(sql))

    async def read_by_course_id(self, id_: UUID4) -> Sequence[UserCourse]:
        sql = self.from_table.select('*').where(self.table.course_id == id_).get_sql()
        return await self._execute_many(text(sql))

    async def count_by_user_id(self, id_: UUID4) -> int:
        sql = self.from_table.select(functions.Count("*")).where(self.table.user_id == id_).get_sql()
        rows = await self.execute_with_return(text(sql))
        return self._get_counter(rows)

    async def count_by_course_id(self, id_: UUID4) -> int:
        sql = self.from_table.select(functions.Count("*")).where(self.table.course_id == id_).get_sql()
        rows = await self.execute_with_return(text(sql))
        return self._get_counter(rows)
