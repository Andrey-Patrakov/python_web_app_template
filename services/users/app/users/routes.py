from fastapi import APIRouter, HTTPException, status
from .schemas import UserSchema
from .schemas import UserRegisterForm, UserLoginForm
from .services import UsersService


router = APIRouter(prefix='/api/users', tags=['Авторизация и аутентификация'])


@router.get('/{id}')
async def get_user(id: int) -> UserSchema:
    user_service = UsersService()
    user = await user_service.read_one(id=id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found.')

    return user


@router.post('/register')
async def register(user_form: UserRegisterForm) -> UserSchema:
    user_service = UsersService()
    return await user_service.register(user_form)


@router.post('/login')
async def login(user_form: UserLoginForm) -> UserSchema:
    user_service = UsersService()
    return await user_service.login(user_form)
