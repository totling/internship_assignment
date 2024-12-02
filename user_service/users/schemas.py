from pydantic import BaseModel, EmailStr, validator
from typing import Optional


class SUserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str

    @classmethod
    @validator('password')
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v


class SUserAuth(BaseModel):
    email: EmailStr
    password: str


class SUserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

    @classmethod
    @validator('password')
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v


class SUser(BaseModel):
    id: int
    name: str
    email: EmailStr
    password: str
    is_admin: bool

    class Config:
        from_attributes = True
