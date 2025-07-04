from fastapi import Request, Response, HTTPException, status

from src.models.users import User
from src.schemas.users import UserRegisterForm, UserLoginForm
from src.schemas.users import UserUpdateForm, UserChangePasswordForm
from src.utils.password import get_password_hash, verify_password
from src.services.unit_of_work import UnitOfWork
from src.services.auth import AuthService


class UsersService:

    def __init__(self, request: Request, response: Response):
        self.request = request
        self.response = response

    async def register(self, user_form: UserRegisterForm) -> User:
        async with UnitOfWork() as uow:
            if await uow.users.read_one(username=user_form.username):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail='There is already another user with this username.')

            if await uow.users.read_one(email=user_form.email):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail='There is already another user with this email.')

            user = user_form.model_dump()
            user['password'] = get_password_hash(user['password'])
            new_user = await uow.users.create(**user)

        return new_user

    async def login(self, user_form: UserLoginForm) -> User:
        email = user_form.email
        password = user_form.password

        async with UnitOfWork() as uow:

            verified = False
            user = await uow.users.get_by_username(email)
            if user:
                verified = verify_password(
                    plain_password=password,
                    hashed_password=user.password)

            if not verified:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail='User not found or password is wrong.')

            auth_service = AuthService(self.request, self.response)
            await auth_service.login(user.id)

        return user

    async def logout(self):
        auth_service = AuthService(self.request, self.response)
        await auth_service.logout()

    async def get_current_user(self) -> User:
        auth_service = AuthService(self.request, self.response)
        user_id = await auth_service.get_current_user_id()
        return await self.get_user_by_id(user_id)

    async def get_user_by_id(self, user_id: int) -> User:
        async with UnitOfWork() as uow:
            return await uow.users.read_one(id=user_id)

    async def update_current(self, user_form: UserUpdateForm) -> User:
        async with UnitOfWork() as uow:
            user = await self.get_current_user()

            form_data = user_form.model_dump()
            if user_form.email != user.email:
                form_data['is_verified'] = False

            await uow.users.update(filter_by={'id': user.id}, **form_data)
            return await uow.users.read_one(id=user.id)

    async def change_password(self, pwd_form: UserChangePasswordForm):
        async with UnitOfWork() as uow:
            user = await self.get_current_user()

            if not verify_password(
                    plain_password=pwd_form.old_password,
                    hashed_password=user.password):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail='Old password is wrong.')

            await uow.users.update(
                filter_by={'id': user.id},
                password=get_password_hash(pwd_form.new_password))
