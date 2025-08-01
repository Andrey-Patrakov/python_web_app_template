from fastapi import APIRouter, HTTPException, status
from datetime import timedelta

from src.config import settings

from src.schemas.users import UserSchema, UserRegisterForm, UserLoginForm
from src.schemas.users import UserUpdateForm, UserChangePasswordForm
from src.schemas.users import UserConfirmForm
from src.schemas.tokens import TokenTypes
from src.api.dependencies import UsersDep, EmailDep, TokenDep


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


@router.post('/verify-email')
async def verify_email(
        users_service: UsersDep,
        email_service: EmailDep,
        token_service: TokenDep):

    user = await users_service.get_current_user()
    token = await token_service.create(
            user_id=user.id,
            expires_delta=timedelta(minutes=settings.LINK_EXPIRE_MINUTES),
            token_type=TokenTypes.VERIFICATION)

    await email_service.send_email_verification_message(user, token)
    return {'message': 'Email verification message sent'}


@router.post('/confirm')
async def confirm(
        confirm_form: UserConfirmForm,
        users_service: UsersDep,
        token_service: TokenDep):

    token = await token_service.get(confirm_form.token)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Token not found')

    await token_service.delete(token.token)
    if token.token_type == TokenTypes.VERIFICATION:
        await users_service.verify_email(token.user_id)
        return {'message': 'Email is verified'}

    raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Token not found')
