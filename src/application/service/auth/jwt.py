from abc import ABC, abstractmethod
from datetime import datetime

import jwt


class IJwtService(ABC):
    @abstractmethod
    def create(self, data: dict) -> str: ...

    @abstractmethod
    def verify(self, token: str) -> dict | None: ...


class JwtService(IJwtService):

    def __init__(self, secret_key: str, expiration_time: int, algorithm: str):
        self.__secret_key = secret_key
        self.__expiration_time = expiration_time
        self.__algorithm = algorithm

    def create(self, data: dict) -> str:
        expiration = datetime.now().timestamp() + self.__expiration_time
        data.update({"exp": expiration})

        return jwt.encode(data, self.__secret_key, algorithm=self.__algorithm)

    def verify(self, token: str) -> dict | None:
        try:
            decoded_data = jwt.decode(token, self.__secret_key, algorithms=[self.__algorithm])
            return decoded_data
        except jwt.PyJWTError:
            return None
