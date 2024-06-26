from abc import ABC, abstractmethod
from enum import Enum
from typing import TypeVar, Iterable, Generic, Any

from pypika import Table, Query, PostgreSQLQuery, Order
from pypika.queries import QueryBuilder
from sqlalchemy import text, Row
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession


IdT = TypeVar("IdT")
ResultT = TypeVar("ResultT")


class AbstractPostgresRepository(ABC, Generic[IdT, ResultT]):

    def __init__(self, session_maker: async_sessionmaker[AsyncSession]):
        self._session_maker = session_maker

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
        return ResultT(**row._mapping)  # noqa

    @classmethod
    def _convert_to_models(cls, rows: Iterable[Row]) -> Iterable[ResultT]:
        return [cls._convert_to_model(row) for row in rows]

    async def _execute_one(self, sql: text) -> ResultT:
        async with self._session_maker() as session:
            result = await session.execute(sql)
            await session.commit()
            row = result.fetchone()
            return self._convert_to_model(row)

    async def _execute_many(self, sql: text) -> Iterable[ResultT]:
        async with self._session_maker() as session:
            result = await session.execute(sql)
            await session.commit()
            rows = result.fetchall()
            return self._convert_to_models(rows)

    async def execute(self, sql: text) -> Iterable[Row]:
        async with self._session_maker() as session:
            result = await session.execute(sql)
            await session.commit()
            return result.fetchall()

    async def read_one(self, id_: IdT) -> ResultT:
        sql = self.from_table.select('*').where(self.table.id == id_).get_sql()
        return await self._execute_one(text(sql))

    async def delete(self, id_: IdT) -> ResultT:
        sql = self.from_table.delete().where(self.table.id == id_).returning("*").get_sql()
        return await self._execute_one(text(sql))

    async def read_many(self, limit: int, offset: int, order: Order, order_by="updated_at") -> Iterable[ResultT]:
        sql = self.from_table.select('*').orderby(order_by, order=order)[limit:offset].get_sql()
        return await self._execute_many(text(sql))
