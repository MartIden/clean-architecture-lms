from dataclasses import dataclass


@dataclass
class UserAnswer:
    login: str
    email: str


@dataclass
class UserInCreateRequest:
    login: str
    email: str
    password: str
