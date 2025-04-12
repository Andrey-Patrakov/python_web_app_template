from fastapi import HTTPException, status
from datetime import datetime, timedelta
from urllib.parse import urlparse, urlencode, urlunsplit

from app.config import settings
from .token import VerificationToken
from .user import UserDAO


async def get_verification_url(user_id: int):
    token = await VerificationToken.create(
        user_id=user_id, expires_delta=timedelta(minutes=30))

    frontend_url = urlparse(settings.FRONTEND_URL)
    path = 'user/verify'
    result = urlunsplit((
        frontend_url.scheme, frontend_url.netloc, path,
        urlencode({'token': token}), ''))

    return result


async def verify_email(token: str):
    token_obj = await VerificationToken.find(token)
    if not token_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Токен не найден.')

    await VerificationToken.delete(token)
    if token_obj.expires_at < datetime.now():
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail='Ссылка устарела, выполните повторную отправку письма.')

    return await UserDAO.verify_email(token_obj.user_id)
