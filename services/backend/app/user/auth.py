from passlib.context import CryptContext
from fastapi import HTTPException, status, Request, Response
from .user import UserDAO
from .token import JWT_Token
from .token import TokenNotFoundError, TokenInvalidError, TokenBlacklistedError
from jose.exceptions import JWTError, ExpiredSignatureError


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def register_user(user: dict):
    if await UserDAO.check_user_exists(
            email=user['email'], username=user['username']):

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Пользователь с таким логином или Email уже существует!')

    user['password'] = get_password_hash(user['password'])
    return await UserDAO.add(**user)


async def authenticate_user(response: Response, email: str, password: str):
    check = False
    user = await UserDAO.get_user_by_email(email=email)
    if user:
        check = verify_password(
            plain_password=password,
            hashed_password=user.password)

    if not check:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Неверный логин или пароль!')

    await JWT_Token.create_access_token(user.id, response=response)
    await JWT_Token.create_refresh_token(user.id, response=response)
    return user


async def logout_user(request: Request, response: Response):
    try:
        await JWT_Token.delete_access_token(request, response)
        await JWT_Token.delete_refresh_token(request, response)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e))

    return {'detail': 'Выход произведен успешно!'}


async def get_current_user(request: Request, response: Response):
    try:
        try:
            user_id = await JWT_Token.get_user_from_access_token(request)
        except ExpiredSignatureError:
            user_id = await JWT_Token.get_user_from_refresh_token(request)
            await JWT_Token.create_access_token(user_id, response)

    except (TokenNotFoundError,
            TokenInvalidError,
            TokenBlacklistedError,
            JWTError) as e:
        await logout_user(request, response)
        error = 'Невалидный токен!' if type(e) is JWTError else str(e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(error))

    user = await UserDAO.find_one_or_none_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Пользователь не найден')

    return user
