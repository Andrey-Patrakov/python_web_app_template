from fastapi import APIRouter, status, Request, Response
from src.core import route
from src.config import settings
from .schemas import UserRegisterForm, UserLoginForm
from .schemas import UserUpdateForm, UserChangePasswordForm


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
    request_method=router.get,
    path='/',
    status_code=status.HTTP_200_OK,
    payload_key=None,
    service_url=settings.SERVICES['users']['url'],
    response_model='services.users.schemas.UserSchema')
async def get_current_user(request: Request, response: Response):
    pass


@route(
    request_method=router.put,
    path='/',
    status_code=status.HTTP_200_OK,
    payload_key='user_form',
    service_url=settings.SERVICES['users']['url'],
    response_model='services.users.schemas.UserSchema')
async def update_current_user(
        user_form: UserUpdateForm,
        request: Request, response: Response):
    pass


@route(
    request_method=router.put,
    path='/change-password',
    status_code=status.HTTP_200_OK,
    payload_key='user_form',
    service_url=settings.SERVICES['users']['url'],
    response_model=None)
async def change_password(
        user_form: UserChangePasswordForm,
        request: Request, response: Response):
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


@route(
    request_method=router.post,
    path='/login',
    status_code=status.HTTP_200_OK,
    payload_key='user_form',
    service_url=settings.SERVICES['users']['url'],
    response_model='services.users.schemas.UserSchema')
async def login(user_form: UserLoginForm,
                request: Request, response: Response):
    pass


@route(
    request_method=router.post,
    path='/logout',
    status_code=status.HTTP_200_OK,
    payload_key=None,
    service_url=settings.SERVICES['users']['url'],
    response_model=None)
async def logout(request: Request, response: Response):
    pass
