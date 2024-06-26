from datetime import datetime
from typing import Type

from pydantic import UUID4
from pypika import PostgreSQLQuery
from sqlalchemy import text

from src.domain.user.dto.user import UserInCreate, UserInUpdate
from src.domain.user.entity.user import User
from src.domain.user.exceptions.exist import UserIsNotExistsError
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

    async def update(self, schema: UserInUpdate) -> User:
        user = await self.read_one(schema.id)

        if not user:
            raise UserIsNotExistsError(f"User with id {schema.id} is not exist")

        roles = self._convert_list_to_postgres_array(
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
