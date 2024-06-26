from datetime import datetime

from pypika import Table, PostgreSQLQuery
from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.domain.user.dto.user import UserInCreate
from src.domain.user.entity.user import User
from src.domain.user.ports.user_repo import IUserRepo


class UserRepo(IUserRepo):

    def __init__(self, session_maker: async_sessionmaker[AsyncSession]):
        self.__session_maker = session_maker

    @property
    def table(self) -> Table:
        return Table("users")

    async def create(self, data: UserInCreate) -> User:
        now = int(datetime.now().timestamp())
        query = PostgreSQLQuery \
            .into(self.table) \
            .columns(
                self.table.login,
                self.table.password,
                self.table.email,
                self.table.roles,
                self.table.created_at,
                self.table.updated_at,
            ) \
            .insert(
                data.login,
                data.password,
                data.email,
                data.roles,
                now,
                now,
            ) \
            .returning("*") \
            .get_sql()

        async with self.__session_maker() as session:
            result = await session.execute(text(query))
            await session.commit()
            row = result.fetchone()
            return User(**row._mapping)
