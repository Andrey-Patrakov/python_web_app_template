from fastapi import APIRouter, Depends, HTTPException, status, Response

from .user import User
from .user import UserDAO
from .user import UserRegisterSchema, UserAuthSchema, UserSchema
from .user import UserUpdateInfoSchema, UserChangePwdSchema

from .auth import get_current_user
from .auth import get_password_hash, verify_password
from .auth import register_user, authenticate_user, logout_user

router = APIRouter(prefix='/user', tags=['Авторизация и аутентификация'])


@router.post('/register')
async def register(user_in: UserRegisterSchema) -> dict:
    user_dict = user_in.model_dump()
    await register_user(user_dict)
    return {'message': 'Вы успешно зарегистрированы!'}


@router.post('/login')
async def login(response: Response, user_data: UserAuthSchema) -> dict:
    await authenticate_user(
        response=response, email=user_data.email, password=user_data.password)

    return {'message': 'Вход выполнен успешно!'}


@router.get('/me')
async def get_me(user_data: User = Depends(get_current_user)) -> UserSchema:
    return user_data


@router.post('/logout')
async def logout(detail: dict = Depends(logout_user)) -> dict:
    return detail


@router.post('/upd_info')
async def update_user_info(
        info: UserUpdateInfoSchema,
        user: User = Depends(get_current_user)) -> dict:

    info_dict = info.model_dump()
    if info.email != user.email:
        info_dict["is_verified"] = False

    await UserDAO.update(filter_by={"id": user.id}, **info_dict)
    return {'message': 'Данные обновлены успешно!'}


@router.post('/change_pwd')
async def change_pwd(
        pwd_form: UserChangePwdSchema,
        user: User = Depends(get_current_user)) -> dict:

    if not verify_password(
            plain_password=pwd_form.old_password,
            hashed_password=user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Неверный пароль!')

    await UserDAO.update(
        filter_by={"id": user.id},
        password=get_password_hash(pwd_form.new_password))

    return {'message': 'Данные обновлены успешно!'}


@router.post('/verify_email')
async def verify_email(
        user: User = Depends(get_current_user)) -> dict:

    # TODO
    return {
        'message': 'Письмо отправлено на указанный адрес электронной почты!'}
