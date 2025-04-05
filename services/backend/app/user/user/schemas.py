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
    description: str | None = Field(..., description="Описание пользователя")
    is_verified: bool = Field(..., description='Подтверждена ли почта')
    created_at: datetime = Field(..., description='Дата создания пользователя')


class UserUpdateInfoSchema(BaseModel):
    email: EmailStr = Field(..., description='Email пользователя')
    username: str = Field(..., description='Логин пользователя')
    description: str | None = Field(..., max_length=1000, description="Описание пользователя") # noqa


class UserChangePwdSchema(BaseModel):
    old_password: str = Field(..., min_length=5, max_length=50, description='Старый пароль') # noqa
    new_password: str = Field(..., min_length=5, max_length=50, description='Новый пароль') # noqa
