from datetime import datetime
from typing import Sequence

from pydantic import UUID4
from pypika import PostgreSQLQuery, Table, JoinType, functions
from sqlalchemy import text

from src.domain.user.dto.user import UserInCreate, UserInUpdate
from src.domain.user.entity.user import User
from src.domain.user.ports.user_repo import IUserRepo
from src.infrastructure.persistence.postgres.repositiries.abstract import AbstractPostgresRepository


class UserRepo(AbstractPostgresRepository[UUID4, User], IUserRepo):

    _result_model = User

    @property
    def table_name(self) -> str:
        return "users"

    async def create(self, schema: UserInCreate) -> User:
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
                schema.login,
                schema.password,
                schema.email,
                schema.roles,
                now,
                now,
            ) \
            .returning("*") \
            .get_sql()

        return await self._execute_one(text(query))

    async def update(self, schema: UserInUpdate) -> User | None:
        user = await self.read_one(schema.id)

        if not user:
            return

        roles = self._convert_iterable_to_postgres_array(
            collection=[role.value for role in schema.roles or user.roles]
        )

        query = PostgreSQLQuery.update(self.table) \
            .set(self.table.login, schema.login or user.login) \
            .set(self.table.email, schema.email or user.email) \
            .set(self.table.password, schema.password or user.password) \
            .set(self.table.roles, roles) \
            .set(self.table.updated_at, int(datetime.now().timestamp())) \
            .where(self.table.id == schema.id) \
            .get_sql()

        await self.execute(text(query))
        return await self.read_one(schema.id)

    async def read_by_login(self, login: str) -> User | None:
        sql = self.from_table.select('*')\
            .where(self.table.login == login)\
            .get_sql()

        return await self._execute_one(text(sql))

    async def read_by_course_id(self, id_: UUID4, limit: int, offset: int, order: str, order_by: str) -> Sequence[User]:
        users_courses_table = Table("users_courses")
        courses_table = Table("courses")

        sql = (
            self.from_table.select(
                self.table.id,
                self.table.login,
                self.table.email,
                self.table.password,
                self.table.roles,
                self.table.updated_at,
                self.table.created_at,
            )
            .join(users_courses_table, JoinType.left)
            .on(self.table.id == users_courses_table.user_id)
            .join(courses_table, JoinType.left)
            .on(users_courses_table.course_id == courses_table.id)
            .where(courses_table.id == id_).get_sql()
        )

        return await self._execute_many(text(sql))

    async def count_by_course_id(self, id_: UUID4) -> int:
        users_courses_table = Table("users_courses")
        courses_table = Table("courses")

        sql = (
            self.from_table.select(functions.Count("*"))
            .join(users_courses_table, JoinType.left)
            .on(self.table.id == users_courses_table.user_id)
            .join(courses_table, JoinType.left)
            .on(users_courses_table.course_id == courses_table.id)
            .where(courses_table.id == id_).get_sql()
        )

        rows = await self.execute_with_return(text(sql))
        return self._get_counter(rows)
