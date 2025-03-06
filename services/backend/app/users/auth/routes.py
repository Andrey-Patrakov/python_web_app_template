from fastapi import APIRouter, Depends, HTTPException, status, Response
from ..user.dao import UsersDAO

from ..user.models import User
from ..user.schemas import UserRegisterSchema, UserAuthSchema, UserSchema
from ..user.schemas import UserUpdateInfoSchema
from .auth import get_password_hash, authenticate_user
from .auth import get_current_user, logout_current_user
from .tokens import create_access_token, create_refresh_token
from .tokens import ACCESS_TOKEN_KEY, REFRESH_TOKEN_KEY, TOKEN_MAX_AGE

router = APIRouter(prefix='/auth', tags=['Авторизация и аутентификация'])


@router.post('/register')
async def register(user_in: UserRegisterSchema) -> dict:
    user = await UsersDAO.check_user_exists(
        email=user_in.email, username=user_in.username)

    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Пользователь с таким логином или Email уже существует!')

    user_dict = user_in.model_dump()
    user_dict['password'] = get_password_hash(user_in.password)
    await UsersDAO.add(**user_dict)

    return {'message': 'Вы успешно зарегистрированы!'}


@router.post('/login')
async def login(response: Response, user_data: UserAuthSchema) -> dict:
    check = await authenticate_user(
        email=user_data.email, password=user_data.password)

    if check is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Неверный логин или пароль!')

    access_token = create_access_token(data={'sub': str(check.id)})
    response.set_cookie(
        key=ACCESS_TOKEN_KEY,
        value=access_token,
        httponly=True,
        secure=True,
        max_age=TOKEN_MAX_AGE)

    refresh_token = create_refresh_token(data={'sub': str(check.id)})
    response.set_cookie(
        key=REFRESH_TOKEN_KEY,
        value=refresh_token,
        httponly=True,
        secure=True,
        max_age=TOKEN_MAX_AGE)

    return {'message': 'Вход выполнен успешно!'}


@router.get('/me')
async def get_me(user_data: User = Depends(get_current_user)) -> UserSchema:
    return user_data


@router.post('/logout')
async def logout(detail: dict = Depends(logout_current_user)) -> dict:
    return detail


@router.post('/upd_info')
async def update_user_info(
        info: UserUpdateInfoSchema,
        user: User = Depends(get_current_user)) -> dict:
    info_dict = info.model_dump()
    await UsersDAO.update(filter_by={"id": user.id}, **info_dict)
    return {'message': 'Данные обновлены успешно!'}
