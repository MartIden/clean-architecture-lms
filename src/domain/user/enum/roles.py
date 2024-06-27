from enum import Enum


class UserRoleEnum(str, Enum):
    STUDENT: str = "STUDENT"
    AUTHOR: str = "AUTHOR"
    TEACHER: str = "TEACHER"
    ADMIN: str = "ADMIN"


ALL_ROLES = {
    UserRoleEnum.ADMIN,
    UserRoleEnum.TEACHER,
    UserRoleEnum.AUTHOR,
    UserRoleEnum.STUDENT,
}
