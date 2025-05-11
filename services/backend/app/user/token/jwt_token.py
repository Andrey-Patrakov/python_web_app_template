from app.config import settings
from datetime import datetime, timedelta
from jose import jwt
from fastapi import Request, Response

from .token import BlacklistedToken

ACCESS_TOKEN_KEY = 'acctok'
ACCESS_TOKEN_EXPIRES_DELTA = timedelta(
    minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

REFRESH_TOKEN_KEY = 'rfshtok'
REFRESH_TOKEN_EXPIRES_DELTA = timedelta(
    days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

TOKEN_MAX_AGE = settings.REFRESH_TOKEN_EXPIRE_DAYS*24*60*60


class TokenNotFoundError(Exception):
    pass


class TokenInvalidError(Exception):
    pass


class TokenBlacklistedError(Exception):
    pass


class JWT_Token:

    @classmethod
    async def create(
            cls, data: dict,
            expires_delta: timedelta | None,
            secret_key: str | None):

        if secret_key is None:
            secret_key = settings.SECRET_KEY

        expires_at = None
        if expires_delta is not None:
            expires_at = datetime.now() + expires_delta

        to_encode = data.copy()
        to_encode.update({'exp': expires_at, 'iat': datetime.now()})

        return jwt.encode(
            to_encode, secret_key, algorithm=settings.ALGORITHM)

    @classmethod
    async def create_access_token(cls, user_id: int, response: Response):
        data = {'sub': str(user_id)}
        secret_key = settings.SECRET_KEY
        token = await cls.create(
            data=data,
            expires_delta=ACCESS_TOKEN_EXPIRES_DELTA,
            secret_key=secret_key)

        response.set_cookie(
            key=ACCESS_TOKEN_KEY,
            value=token,
            httponly=settings.SECURE,
            secure=settings.SECURE,
            max_age=TOKEN_MAX_AGE)

        return token

    @classmethod
    async def create_refresh_token(cls, user_id: int, response: Response):
        data = {'sub': str(user_id)}
        secret_key = settings.SECRET_KEY
        token = await cls.create(
            data=data,
            expires_delta=REFRESH_TOKEN_EXPIRES_DELTA,
            secret_key=secret_key)

        response.set_cookie(
            key=REFRESH_TOKEN_KEY,
            value=token,
            httponly=settings.SECURE,
            secure=settings.SECURE,
            max_age=TOKEN_MAX_AGE)

        return token

    @classmethod
    async def _get_token(cls, request: Request, token_key: str):
        token = request.cookies.get(token_key)
        if not token:
            raise TokenNotFoundError('Токен не найден')

        return token

    @classmethod
    async def get_access_token(cls, request: Request):
        return await cls._get_token(request, ACCESS_TOKEN_KEY)

    @classmethod
    async def get_refresh_token(cls, request: Request):
        return await cls._get_token(request, REFRESH_TOKEN_KEY)

    @classmethod
    async def _get_user_from_token(cls, token: str, secret_key: str):
        payload = jwt.decode(
            token, secret_key, algorithms=[settings.ALGORITHM])

        user_id = payload.get('sub')
        if user_id is None:
            raise TokenInvalidError('Не найден ID пользователя')

        if await BlacklistedToken.find(token):
            raise TokenBlacklistedError('Токен был отозван')

        return int(user_id)

    @classmethod
    async def get_user_from_access_token(cls, request: Request):
        token = await cls.get_access_token(request)
        secret_key = settings.SECRET_KEY
        return await cls._get_user_from_token(token, secret_key)

    @classmethod
    async def get_user_from_refresh_token(cls, request: Request):
        token = await cls.get_refresh_token(request)
        secret_key = settings.SECRET_KEY
        return await cls._get_user_from_token(token, secret_key)

    @classmethod
    async def delete_access_token(cls, request: Request, response: Response):
        token = await cls.get_access_token(request)
        user = await cls.get_user_from_access_token(request)
        await BlacklistedToken.add(token, user, ACCESS_TOKEN_EXPIRES_DELTA)
        response.delete_cookie(ACCESS_TOKEN_KEY)
        return token

    @classmethod
    async def delete_refresh_token(cls, request: Request, response: Response):
        token = await cls.get_refresh_token(request)
        user = await cls.get_user_from_refresh_token(request)
        await BlacklistedToken.add(token, user, REFRESH_TOKEN_EXPIRES_DELTA)
        response.delete_cookie(REFRESH_TOKEN_KEY)
        return token
