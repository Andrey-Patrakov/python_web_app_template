from fastapi import HTTPException, status
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from datetime import datetime, timedelta
from urllib.parse import urlparse, urlencode, urlunsplit

from app.config import settings
from .token import PasswordRestoreToken
from .user import UserDAO
from .auth import get_password_hash


async def get_pwd_restore_url(user_id: int):
    token = await PasswordRestoreToken.create(
        user_id=user_id, expires_delta=timedelta(minutes=30))

    frontend_url = urlparse(
        f'{settings.FRONTEND_HOST}:{settings.FRONTEND_PORT}')

    path = 'user/restore-pwd'
    link = urlunsplit((
        frontend_url.scheme, frontend_url.netloc, path,
        urlencode({'token': token}), ''))

    return link, frontend_url.netloc


def create_message(link, sitename):
    path = Path(__file__).parent / 'templates'
    environment = Environment(loader=FileSystemLoader(path))
    template = environment.get_template('restore_pwd.html')
    return template.render(sitename=sitename, link=link)


async def change_password(token: str, new_password: str):
    token_obj = await PasswordRestoreToken.find(token)
    if not token_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Ссылка устарела, выполните повторную отправку письма.')

    await PasswordRestoreToken.delete(token)
    timezone = token_obj.expires_at.astimezone().tzinfo
    if token_obj.expires_at < datetime.now(timezone):
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail='Ссылка устарела, выполните повторную отправку письма.')

    return await UserDAO.update(
        filter_by={"id": token_obj.user_id},
        password=get_password_hash(new_password))
