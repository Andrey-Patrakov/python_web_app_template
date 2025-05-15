from fastapi import HTTPException, status
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from datetime import datetime, timedelta
from urllib.parse import urlparse, urlencode, urlunsplit

from app.config import settings
from .token import VerificationToken
from .user import UserDAO


async def get_verification_url(user_id: int):
    token = await VerificationToken.create(
        user_id=user_id, expires_delta=timedelta(minutes=30))

    frontend_url = urlparse(
        f'{settings.FRONTEND_HOST}:{settings.FRONTEND_PORT}')

    path = 'user/verify'
    link = urlunsplit((
        frontend_url.scheme, frontend_url.netloc, path,
        urlencode({'token': token}), ''))

    return link, frontend_url.netloc


def create_message(link, sitename):
    path = Path(__file__).parent / 'templates'
    environment = Environment(loader=FileSystemLoader(path))
    template = environment.get_template('email_verification.html')
    return template.render(sitename=sitename, link=link)


async def verify_email(token: str):
    token_obj = await VerificationToken.find(token)
    if not token_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Токен не найден.')

    await VerificationToken.delete(token)
    timezone = token_obj.expires_at.astimezone().tzinfo
    if token_obj.expires_at < datetime.now(timezone):
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail='Ссылка устарела, выполните повторную отправку письма.')

    return await UserDAO.verify_email(token_obj.user_id)
