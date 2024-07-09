from datetime import datetime
from typing import Sequence

from pydantic import UUID4
from pypika import PostgreSQLQuery, functions
from sqlalchemy import text

from src.domain.lesson.dto.lesson import LessonInUpdate, LessonInCreate
from src.domain.lesson.entity.lesson import Lesson
from src.domain.lesson.port.lesson_repo import ILessonRepo
from src.infrastructure.persistence.postgres.repositiries.abstract import AbstractPostgresRepository


class LessonRepo(AbstractPostgresRepository[UUID4, Lesson], ILessonRepo):

    _result_model = Lesson

    @property
    def table_name(self) -> str:
        return "lessons"

    async def create(self, schema: LessonInCreate) -> Lesson:
        now = int(datetime.now().timestamp())

        query = PostgreSQLQuery \
            .into(self.table) \
            .columns(
                self.table.title,
                self.table.description,
                self.table.content,
                self.table.cover,
                self.table.course_id,
                self.table.created_at,
                self.table.updated_at,
            ) \
            .insert(
                schema.title,
                schema.description,
                schema.content,
                schema.cover,
                schema.course_id,
                now,
                now,
            ) \
            .returning("*") \
            .get_sql()

        return await self._execute_one(text(query))

    async def update(self, schema: LessonInUpdate) -> Lesson | None:
        lesson = await self.read_one(schema.id)

        if not lesson:
            return

        query = PostgreSQLQuery.update(self.table) \
            .set(self.table.title, schema.title or lesson.login) \
            .set(self.table.description, schema.description or lesson.email) \
            .set(self.table.content, schema.content or lesson.password) \
            .set(self.table.cover, schema.cover or lesson.password) \
            .set(self.table.course_id, schema.course_id or lesson.password) \
            .set(self.table.updated_at, int(datetime.now().timestamp())) \
            .where(self.table.id == schema.id) \
            .get_sql()

        await self.execute(text(query))
        return await self.read_one(schema.id)

    async def read_by_course(self, id_: UUID4) -> Sequence[Lesson]:
        sql = self.from_table.select('*').where(self.table.course_id == id_).get_sql()
        return await self._execute_many(text(sql))

    async def count_by_course(self, id_: UUID4) -> Sequence[Lesson]:
        sql = self.from_table.select(functions.Count("*")).where(self.table.course_id == id_).get_sql()
        rows = await self.execute_with_return(text(sql))

        if row := rows[0] if rows else None:
            if elem := row[0] if row else None:
                return elem

        return 0

