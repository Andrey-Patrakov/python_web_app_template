from enum import Enum, unique
from datetime import datetime
from pydantic import BaseModel, Field


@unique
class TokenTypes(int, Enum):
    BASE = 0
    BLACKLISTED = 1
    VERIFICATION = 2
    PASSWORD_RESTORE = 3


class TokenSchema(BaseModel):
    token: str = Field(..., description='Токен')
    expires_at: datetime | None = Field(None, description='Срок жизни токена')
    token_type: TokenTypes = Field(TokenTypes.BASE, description='Тип токена') # noqa
    user_id: int = Field(..., description='Идентификатор пользователя')
