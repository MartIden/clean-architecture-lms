from enum import Enum


class Order(str, Enum):
    asc = "ASC"
    desc = "DESC"
