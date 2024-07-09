from abc import ABC, abstractmethod
from typing import TypeVar, Iterable, Generic, Type, Sequence, Any

from pydantic import BaseModel
from pypika import Table, PostgreSQLQuery, functions, Order
from pypika.queries import QueryBuilder
from sqlalchemy import text, Row

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

IdT = TypeVar("IdT", bound=BaseModel)
ResultT = TypeVar("ResultT", bound=BaseModel)


class AbstractPostgresRepository(Generic[IdT, ResultT], ABC):

    _result_model: Type[ResultT]

    def __init__(self, async_session_maker: async_sessionmaker[AsyncSession]):
        self._async_session_maker = async_session_maker

    @property
    @abstractmethod
    def table_name(self) -> str: ...

    @property
    def table(self) -> Table:
        return Table(self.table_name)

    @property
    def from_table(self) -> QueryBuilder:
        return PostgreSQLQuery.from_(self.table)

    @classmethod
    def _convert_to_model(cls, row: Row) -> ResultT:
        return cls._result_model(**row._mapping)  # noqa

    @classmethod
    def _convert_to_models(cls, rows: Iterable[Row]) -> Sequence[ResultT]:
        return [cls._convert_to_model(row) for row in rows]

    async def _execute_one(self, sql: text) -> ResultT | None:
        async with self._async_session_maker() as session:
            result = await session.execute(sql)

            if row := result.fetchone():
                await session.commit()
                return self._convert_to_model(row)

    async def _execute_many(self, sql: text) -> Sequence[ResultT]:
        async with self._async_session_maker() as session:
            result = await session.execute(sql)
            rows = result.fetchall()
            await session.commit()
            return self._convert_to_models(rows)

    async def execute_with_return(self, sql: text) -> Sequence[Row]:
        async with self._async_session_maker() as session:
            result = await session.execute(sql)
            rows = result.fetchall()
            await session.commit()
            return rows

    async def execute(self, sql: text) -> None:
        async with self._async_session_maker() as session:
            await session.execute(sql)
            await session.commit()

    async def read_one(self, id_: IdT) -> ResultT | None:
        sql = self.from_table.select('*').where(self.table.id == id_).get_sql()
        return await self._execute_one(text(sql))

    async def delete(self, id_: IdT) -> ResultT | None:
        if await self.read_one(id_):
            sql = self.from_table.delete().where(self.table.id == id_).returning("*").get_sql()
            return await self._execute_one(text(sql))

    async def read_many(self, limit: int, offset: int, order: Order, order_by="updated_at") -> Sequence[ResultT]:
        sql = self.from_table.select('*').orderby(order_by, order=order)[offset:limit].get_sql()
        return await self._execute_many(text(sql))

    async def count(self) -> int:
        sql = self.from_table.select(functions.Count("*")).get_sql()
        rows = await self.execute_with_return(text(sql))
        return self._get_counter(rows)

    @classmethod
    def _convert_iterable_to_postgres_array(cls, collection: Sequence[Any]) -> str:
        roles = ",".join([f"{str(item)}" for item in collection])
        return '{{{0}}}'.format(roles)

    @classmethod
    def _get_counter(cls, rows: Sequence[Row]) -> int:
        if row := rows[0] if rows else None:
            if elem := row[0] if row else None:
                return elem
        return 0
