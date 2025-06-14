from fastapi import APIRouter, status, Request, Response
from app.core import route
from app.config import settings
from .schemas import UserRegisterForm


router = APIRouter(prefix='/api/users', tags=['Авторизация и аутентификация'])


@route(
    request_method=router.get,
    path='/{id}',
    status_code=status.HTTP_200_OK,
    payload_key=None,
    service_url=settings.SERVICES['users']['url'],
    response_model='services.users.schemas.UserSchema')
async def get_user(id: int, request: Request, response: Response):
    pass


@route(
    request_method=router.post,
    path='/register',
    status_code=status.HTTP_200_OK,
    payload_key='user_form',
    service_url=settings.SERVICES['users']['url'],
    response_model='services.users.schemas.UserSchema')
async def register(user_form: UserRegisterForm,
                   request: Request, response: Response):
    pass
