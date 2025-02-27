from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict, EmailStr


class UserRegisterSchema(BaseModel):
    email: EmailStr = Field(..., description='Email пользователя')
    username: str = Field(..., description='Логин пользователя')
    password: str = Field(..., min_length=5, max_length=50, description='Пароль пользователя') # noqa


class UserAuthSchema(BaseModel):
    email: str = Field(..., description='Email или логин пользователя')
    password: str = Field(..., min_length=5, max_length=50, description='Пароль пользователя') # noqa


class UserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description='Идентификатор пользователя')
    email: EmailStr = Field(..., description='Email пользователя')
    username: str = Field(..., description='Логин пользователя')
    is_active: bool = Field(..., description='Активен ли пользователь')
    created_at: datetime = Field(..., description='Дата создания пользователя')
