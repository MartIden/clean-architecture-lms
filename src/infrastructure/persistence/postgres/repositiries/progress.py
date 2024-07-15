from pydantic import UUID4

from src.domain.progress.dto.progress import ProgressInCreate, ProgressInUpdate
from src.domain.progress.entity.progress import Progress
from src.domain.progress.ports.progress_repo import IProgressRepo
from src.infrastructure.persistence.postgres.repositiries.abstract import AbstractPostgresRepository


class ProgressRepo(AbstractPostgresRepository[UUID4, ProgressInCreate, ProgressInUpdate, Progress], IProgressRepo):

    _result_model = Progress

    @property
    def table_name(self) -> str:
        return "progress"
