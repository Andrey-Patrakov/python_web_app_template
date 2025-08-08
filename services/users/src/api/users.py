from fastapi import APIRouter, HTTPException, status
from fastapi import UploadFile, File
from datetime import timedelta

from src.config import settings

from src.schemas.users import UserSchema, UserRegisterForm, UserLoginForm
from src.schemas.users import UserUpdateForm, UserChangePasswordForm
from src.schemas.users import UserConfirmForm, UserResporePasswordForm
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


@router.post('/restore-password')
async def restore_password(
        restore_pwd_form: UserResporePasswordForm,
        users_service: UsersDep,
        email_service: EmailDep,
        token_service: TokenDep):

    user = await users_service.get_user_by_email(restore_pwd_form.email)
    token = await token_service.create(
            user_id=user.id,
            expires_delta=timedelta(minutes=settings.LINK_EXPIRE_MINUTES),
            token_type=TokenTypes.PASSWORD_RESTORE)

    await email_service.send_restore_password_message(user, token)
    return {'message': 'Password restore message sent'}


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

    if token.token_type == TokenTypes.PASSWORD_RESTORE:
        if not confirm_form.password:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail='Password field is empty in form')

        await users_service.resore_password(
            user_id=token.user_id,
            new_password=confirm_form.password)
        return {'message': 'Password changed'}

    raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Token not found')


@router.put('/avatar')
async def change_avatar(
        users_service: UsersDep,
        file: UploadFile = File()):

    await users_service.change_avatar(file)
    return {'message': 'Avatar changed'}
