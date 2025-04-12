import secrets
from datetime import datetime, timedelta
from .models import Token as TokenModel
from .dao import TokenDAO


BASE_TOKEN = 0
BLACKLISTED_TOKEN = 1


class Token:
    TOKEN_TYPE = BASE_TOKEN

    @classmethod
    async def create(
            cls, user_id: int,
            expires_delta: timedelta | None = None) -> TokenModel | None:

        token = secrets.token_urlsafe()
        return await cls.add(token, user_id, expires_delta)

    @classmethod
    async def add(
            cls, token: str,
            user_id: int,
            expires_delta: timedelta | None = None) -> TokenModel | None:

        expires_at = None
        if expires_delta is not None:
            expires_at = datetime.now() + expires_delta

        result = await TokenDAO.add_token(
            user_id=user_id,
            token=token,
            expires_at=expires_at,
            token_type=cls.TOKEN_TYPE)

        if result is not None:
            return result.token

        return None

    @classmethod
    async def find(cls, token: str) -> TokenModel | None:
        return await TokenDAO.find_one_or_none(
            token=token, token_type=cls.TOKEN_TYPE)

    @classmethod
    async def clear_dead_tokens(cls, token_type: int = None) -> int:
        now = datetime.now()
        flt = {} if token_type is None else {'token_type': token_type}
        return await TokenDAO.delete(
            where=(TokenModel.expires_at < now), **flt)


class BlacklistedToken(Token):
    TOKEN_TYPE = BLACKLISTED_TOKEN
