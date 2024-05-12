from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class OrmMode(BaseModel):
    class Config:
        from_attributes = True


class UserBaseSchema(OrmMode):
    name: Optional[str]
    email: EmailStr
    password: str


class CreateUserSchema(UserBaseSchema):
    pass


class LoginUserSchema(UserBaseSchema):
    pass


class UpdateUserEmailSchema(OrmMode):
    email: EmailStr


class UpdateUserPasswordSchema(OrmMode):
    password: Optional[str]


class UserResponseSchema(OrmMode):
    name: Optional[str]
    email: EmailStr
    created_at: datetime
    updated_at: datetime


class TokenSchema(BaseModel):
    access_token: str
    token_type: str = 'bearer'


class Address(OrmMode):
    address: Optional[str]