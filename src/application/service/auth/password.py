from abc import ABC, abstractmethod

from passlib.context import CryptContext


class IPasswordService(ABC):

    @abstractmethod
    def hash(self, password) -> str: ...

    @abstractmethod
    def verify(self, password: str, hashed_password: str) -> bool: ...


class PasswordService(IPasswordService):

    def __init__(self, pwd_context: CryptContext):
        self.__pwd_context = pwd_context

    def hash(self, password) -> str:
        return self.__pwd_context.hash(password)

    def verify(self, password: str, hashed_password: str) -> bool:
        return self.__pwd_context.verify(password, hashed_password)
