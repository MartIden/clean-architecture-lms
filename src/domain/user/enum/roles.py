from enum import Enum


class UserRoleEnum(str, Enum):
    STUDENT: str = "STUDENT"
    AUTHOR: str = "AUTHOR"
    TEACHER: str = "TEACHER"
