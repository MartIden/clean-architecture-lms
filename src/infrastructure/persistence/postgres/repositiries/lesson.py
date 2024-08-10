from datetime import datetime
from typing import Sequence

from pydantic import UUID4
from pypika import PostgreSQLQuery, functions
from sqlalchemy import text

from src.domain.lesson.dto.lesson import LessonInUpdate, LessonInCreate
from src.domain.lesson.entity.lesson import Lesson
from src.domain.lesson.port.lesson_repo import ILessonRepo
from src.infrastructure.persistence.postgres.repositiries.abstract import AbstractPostgresRepository


class LessonRepo(AbstractPostgresRepository[UUID4, LessonInCreate, LessonInUpdate, Lesson], ILessonRepo):

    _result_model = Lesson

    @property
    def table_name(self) -> str:
        return "lessons"

    async def read_by_course(self, id_: UUID4) -> Sequence[Lesson]:
        sql = self.from_table.select('*').where(self.table.course_id == id_).get_sql()
        return await self._execute_many(text(sql))

    async def count_by_course(self, id_: UUID4) -> int:
        sql = self.from_table.select(functions.Count("*")).where(self.table.course_id == id_).get_sql()
        rows = await self.execute_with_return(text(sql))

        if row := rows[0] if rows else None:
            if elem := row[0] if row else None:
                return elem

        return 0
