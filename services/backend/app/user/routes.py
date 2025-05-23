from PIL import Image
from io import BytesIO
from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi import UploadFile, File

from .user import User
from .user import UserDAO
from .user import UserRegisterSchema, UserAuthSchema, UserSchema
from .user import UserUpdateInfoSchema, UserChangePwdSchema

from .auth import get_current_user
from .auth import get_password_hash, verify_password
from .auth import register_user, authenticate_user, logout_user
from .email_verification import get_verification_url, create_message
from .email_verification import verify_email
from .token import EmailVerificationSchema

from app.mail import SMTP_Mail
from app.storage import Storage

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


@router.post('/send_message')
async def send_message(user: User = Depends(get_current_user)) -> dict:
    link, sitename = await get_verification_url(user.id)
    with SMTP_Mail() as mail:
        message = mail.message(
            user.email, 'Для завершения регистрации подтвердите свой email')

        message.attach_html(create_message(link, sitename))
        message.send()

    return {
        'message': 'Письмо отправлено на указанный адрес электронной почты!'}


@router.post('/verify_email')
async def verify(params: EmailVerificationSchema):
    await verify_email(params.token)
    return {
        'message': 'Подтверждение электронной почты завершено успешно!'}


@router.post('/change_avatar')
async def change_avatar(
        file: UploadFile = File(),
        user: User = Depends(get_current_user)):

    storage = Storage()
    if user.avatar:
        storage.delete(user.avatar)

    try:
        image_io = BytesIO()
        image = Image.open(file.file)

        center_x = image.size[0] // 2
        center_y = image.size[1] // 2
        min_size = min(image.size) // 2

        image = image.crop((
            center_x - min_size,
            center_y - min_size,
            center_x + min_size,
            center_y + min_size))

        image.thumbnail((256, 256))

        image.save(image_io, 'PNG', quality=50)
        image_io.seek(0)

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail='Не удалось обработать изображение!')

    storage_id = storage.upload(
        file=image_io, length=image_io.getbuffer().nbytes)

    await UserDAO.update(filter_by={'id': user.id}, avatar=storage_id)

    return {'message': 'Аватар изменен успешно!'}
