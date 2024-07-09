import asyncio
import functools
import os
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor
from typing import Callable, TypeVar

import bcrypt
from typing_extensions import ParamSpec


class IPasswordService(ABC):

    @abstractmethod
    async def hash(self, password) -> str: ...

    @abstractmethod
    async def verify(self, password: str, hashed_password: str) -> bool: ...


P = ParamSpec("P")
R = TypeVar("R")

pool = ThreadPoolExecutor(
    max_workers=os.cpu_count() or 1,
    thread_name_prefix="AsyncBcryptService",
)


class AsyncBcryptService:
    @classmethod
    def _to_aio(cls, fn: Callable[P, R]) -> Callable[P, "asyncio.Future[R]"]:
        @functools.wraps(fn)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> "asyncio.Future[R]":
            loop = asyncio.get_running_loop()
            return loop.run_in_executor(
                pool, functools.partial(fn, *args, **kwargs)
            )

        return wrapper

    @property
    def gen_salt(self) -> Callable:
        return self._to_aio(bcrypt.gensalt)

    @property
    def hash_pw(self) -> Callable:
        return self._to_aio(bcrypt.hashpw)

    @property
    def check_pw(self) -> Callable:
        return self._to_aio(bcrypt.checkpw)


class PasswordService(IPasswordService):

    def __init__(self, async_bcrypt: AsyncBcryptService) -> None:
        self.__bcrypt = async_bcrypt

    async def hash(self, password: str) -> str:
        salt = await self.__bcrypt.gen_salt(rounds=12, prefix=b"2b")
        return await self.__bcrypt.hash_pw(str.encode(password), salt)

    async def verify(self, password: str, hashed_password: str) -> bool:
        return await self.__bcrypt.check_pw(str.encode(password), str.encode(hashed_password))
