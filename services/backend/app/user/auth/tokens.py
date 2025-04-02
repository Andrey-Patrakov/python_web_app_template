from app.config import settings
from datetime import datetime, timedelta, timezone
from jose import jwt
from fastapi import HTTPException, status, Request

from .dao import AuthDAO

ACCESS_TOKEN_KEY = 'acctok'
REFRESH_TOKEN_KEY = 'rfshtok'
TOKEN_MAX_AGE = settings.REFRESH_TOKEN_EXPIRE_DAYS*24*60*60


class TokenInvalidError(Exception):
    pass


class TokenBlacklistedError(Exception):
    pass


def create_token(
        data: dict,
        expires_delta: timedelta | None,
        **kwargs) -> str:

    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(**kwargs)

    to_encode.update({'exp': expire, 'iat': datetime.now(timezone.utc)})
    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM)


def create_access_token(
        data: dict,
        expires_delta: timedelta | None = None) -> str:
    return create_token(
        data, expires_delta, minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)


def create_refresh_token(
        data: dict,
        expires_delta: timedelta | None = None) -> str:
    return create_token(
        data, expires_delta, days=settings.REFRESH_TOKEN_EXPIRE_DAYS)


async def get_token(request: Request, token_key):
    token = request.cookies.get(token_key)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='Токен не найден')

    return token


async def get_access_token(request: Request):
    return await get_token(request, ACCESS_TOKEN_KEY)


async def get_refresh_token(request: Request):
    return await get_token(request, REFRESH_TOKEN_KEY)


async def check_token(token: str):

    payload = jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=[settings.ALGORITHM])

    user_id = payload.get('sub')
    if user_id is None:
        raise TokenInvalidError('Не найден ID пользователя')

    blacklisted = await AuthDAO.find_one_or_none(token=token)
    if blacklisted:
        raise TokenBlacklistedError('Токен был отозван')

    return user_id
