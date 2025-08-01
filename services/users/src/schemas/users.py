from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict, EmailStr


class UserRegisterForm(BaseModel):
    email: EmailStr = Field(..., description='Email пользователя')
    username: str = Field(..., description='Логин пользователя')
    password: str = Field(..., min_length=5, max_length=50, description='Пароль пользователя') # noqa


class UserLoginForm(BaseModel):
    email: str = Field(..., description='Email или логин пользователя')
    password: str = Field(..., min_length=5, max_length=50, description='Пароль пользователя') # noqa


class UserUpdateForm(BaseModel):
    email: EmailStr = Field(..., description='Email пользователя')
    username: str = Field(..., description='Логин пользователя')
    description: str | None = Field(..., max_length=1000, description="Описание пользователя") # noqa


class UserChangePasswordForm(BaseModel):
    old_password: str = Field(..., min_length=5, max_length=50, description='Старый пароль') # noqa
    new_password: str = Field(..., min_length=5, max_length=50, description='Новый пароль') # noqa


class UserConfirmForm(BaseModel):
    token: str = Field(..., description='Токен, который был отправлен на почту') # noqa


class UserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description='Идентификатор пользователя')
    email: EmailStr = Field(..., description='Email пользователя')
    username: str = Field(..., description='Логин пользователя')
    description: str | None = Field(..., description="Описание пользователя")
    is_verified: bool = Field(..., description='Подтверждена ли почта')
    created_at: datetime = Field(..., description='Дата создания пользователя')
    avatar: str | None = Field(..., description='Идентификатор аватара в хранилище') # noqa
