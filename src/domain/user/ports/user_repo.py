from abc import ABC, abstractmethod

from src.domain.user.dto.user import UserInCreate
from src.domain.user.entity.user import User


class IUserRepo(ABC):
    @abstractmethod
    async def create(self, data: UserInCreate) -> User: ...
