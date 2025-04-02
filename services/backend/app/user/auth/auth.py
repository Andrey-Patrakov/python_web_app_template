from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status, Response
from .tokens import create_access_token
from .tokens import get_access_token, get_refresh_token, check_token
from .tokens import ACCESS_TOKEN_KEY, REFRESH_TOKEN_KEY, TOKEN_MAX_AGE
from .tokens import TokenInvalidError, TokenBlacklistedError
from jose.exceptions import JWTError, ExpiredSignatureError

from .dao import AuthDAO
from ..user.dao import UsersDAO

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def authenticate_user(email: str, password: str):
    user = await UsersDAO.get_user_by_email(email=email)
    if not user:
        return None

    if not verify_password(plain_password=password,
                           hashed_password=user.password):
        return None

    return user


async def logout_current_user(
        response: Response,
        token: str = Depends(get_access_token),
        refresh_token: str = Depends(get_refresh_token)):

    await AuthDAO.add_token_to_blacklist(token=token)
    await AuthDAO.add_token_to_blacklist(token=refresh_token)
    response.delete_cookie(key=ACCESS_TOKEN_KEY)
    response.delete_cookie(key=REFRESH_TOKEN_KEY)

    return {'detail': 'Выход произведен успешно!'}


async def get_current_user(
        response: Response,
        token: str = Depends(get_access_token),
        refresh_token: str = Depends(get_refresh_token)):

    try:
        try:
            user_id = await check_token(token)
        except ExpiredSignatureError:
            user_id = await check_token(refresh_token)
            access_token = create_access_token(data={'sub': str(user_id)})
            response.set_cookie(
                key=ACCESS_TOKEN_KEY,
                value=access_token,
                httponly=True,
                secure=True,
                max_age=TOKEN_MAX_AGE)

    except (TokenInvalidError, TokenBlacklistedError, JWTError) as e:
        await logout_current_user(response, token, refresh_token)
        error = str(e)
        if type(e) is JWTError:
            error = 'Невалидный токен'

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(error))

    user = await UsersDAO.find_one_or_none_by_id(int(user_id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Пользователь не найден')

    return user
