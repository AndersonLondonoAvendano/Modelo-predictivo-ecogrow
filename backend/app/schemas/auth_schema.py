import uuid
from pydantic import BaseModel, ConfigDict, EmailStr

from backend.app.schemas.common import Password


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: Password


class UserLogin(BaseModel):
    email: EmailStr
    password: Password


class UserResponse(UserBase):
    id: uuid.UUID
    role: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"