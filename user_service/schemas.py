from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional

from exceptions import PasswordLengthException


class SUserAuth(BaseModel):
    email: EmailStr
    password: str


class SUserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

    @field_validator('password', mode="before")
    @classmethod
    def password_strength(cls, v: str) -> str:
        if len(v) < 8:
            raise PasswordLengthException
        return v


class SUserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None

    @field_validator('password', mode="before")
    @classmethod
    def password_strength(cls, v: str) -> str:
        if len(v) < 8:
            raise PasswordLengthException
        return v


class SUser(BaseModel):
    id: int
    name: str
    email: EmailStr
    password: str
    is_admin: bool

    class Config:
        from_attributes = True
