from enum import Enum


class UserRoleEnum(str, Enum):
    STUDENT: "UserRoleEnum" = "STUDENT"
    AUTHOR:  "UserRoleEnum" = "AUTHOR"
    TEACHER: "UserRoleEnum" = "TEACHER"
    ADMIN:   "UserRoleEnum" = "ADMIN"


ALL_ROLES = {
    UserRoleEnum.ADMIN,
    UserRoleEnum.TEACHER,
    UserRoleEnum.AUTHOR,
    UserRoleEnum.STUDENT,
}
