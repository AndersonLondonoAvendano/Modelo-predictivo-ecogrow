import enum


class UserStatus(str, enum.Enum):
    user = "user"
    admin = "admin"