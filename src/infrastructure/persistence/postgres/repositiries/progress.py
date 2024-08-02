from typing import Sequence

from pydantic import UUID4
from sqlalchemy import text

from src.domain.progress.dto.progress import ProgressInCreate, ProgressInUpdate
from src.domain.progress.entity.progress import Progress
from src.domain.progress.ports.progress_repo import IProgressRepo
from src.infrastructure.persistence.postgres.repositiries.abstract import AbstractPostgresRepository


class ProgressRepo(AbstractPostgresRepository[UUID4, ProgressInCreate, ProgressInUpdate, Progress], IProgressRepo):

    _result_model = Progress

    @property
    def table_name(self) -> str:
        return "progress"

    async def get_by_course(self, course_id: UUID4, user_id: UUID4) -> Sequence[Progress]:
        sql = (
            self.from_table.select('*')
            .where(self.table.course_id == course_id)
            .where(self.table.user_id == user_id)
            .get_sql()
        )
        
        return await self._execute_many(text(sql))
