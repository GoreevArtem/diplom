from datetime import datetime
from enum import Enum
from typing import List, Optional, Union

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


class StatusOrder(str, Enum):
    DELIVERED: str = "delivered"
    INPROCESS: str = "in process"


class Order(OrmMode):
    date: datetime
    status: StatusOrder
    address: Address

# Модель данных для рецепта
class Recipe(BaseModel):
    recipe_name: str
    ingredients: List[str]
    instructions: str
    photo: Union[str, None]

class Image(BaseModel):
    url: str