from fastapi import APIRouter
from src.schemas.users import UserSchema, UserRegisterForm, UserLoginForm
from src.schemas.users import UserUpdateForm, UserChangePasswordForm
from src.api.dependencies import UsersDep


router = APIRouter(
    prefix='/api/users',
    tags=['Авторизация и аутентификация'])


@router.get('/{id}')
async def get_user(id: int, users_service: UsersDep) -> UserSchema:
    return await users_service.get_user_by_id(id)


@router.get('/')
async def get_current_user(users_service: UsersDep) -> UserSchema:
    return await users_service.get_current_user()


@router.put('/')
async def update_current_user(
        user_form: UserUpdateForm, users_service: UsersDep) -> UserSchema:
    return await users_service.update_current(user_form)


@router.put('/change-password')
async def change_password(
        user_form: UserChangePasswordForm, users_service: UsersDep) -> dict:
    await users_service.change_password(user_form)
    return {'message': 'Password changed.'}


@router.post('/register')
async def register(
        user_form: UserRegisterForm, users_service: UsersDep) -> UserSchema:
    return await users_service.register(user_form)


@router.post('/login')
async def login(
        user_form: UserLoginForm, users_service: UsersDep) -> UserSchema:
    return await users_service.login(user_form)


@router.post('/logout')
async def logout(users_service: UsersDep) -> dict:
    await users_service.logout()
    return {'message': 'Logged out'}
