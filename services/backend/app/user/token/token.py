import secrets
from .models import Token as TokenModel
from ..user.models import User
from datetime import datetime, timedelta
from .dao import TokenDAO


BASE_TOKEN = 0


class Token:

    TOKEN_TYPE = BASE_TOKEN

    async def create(
            self, user: User,
            expires_delta: timedelta | None = None) -> TokenModel | None:

        token = secrets.token_urlsafe()
        expires_at = None
        if expires_delta is not None:
            expires_at = datetime.now() + expires_delta

        result = await TokenDAO.add(
            user_id=user.id,
            token=token,
            expires_at=expires_at,
            token_type=self.TOKEN_TYPE)

        if result is not None:
            return result.token

        return None

    async def find(self, token: str) -> TokenModel | None:
        return await TokenDAO.find_one_or_none(token=token)

    async def clear_dead(self, token_type: int = None) -> int:
        now = datetime.now()
        flt = {} if token_type is None else {'token_type': token_type}
        return await TokenDAO.delete(
            where=(TokenModel.expires_at < now), **flt)
