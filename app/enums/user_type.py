from enum import Enum


class UserType(str, Enum):
    admin = "admin"
    user = "user"