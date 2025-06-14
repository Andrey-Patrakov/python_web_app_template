from fastapi import HTTPException, status
from database import SQLAlchemyService, UnitOfWork
from .repositories import UserRepository
from .models import User
from .schemas import UserRegisterForm, UserLoginForm
from ..utils.password import get_password_hash, verify_password


class UsersService(SQLAlchemyService):
    repository = UserRepository

    async def register(self, user_form: UserRegisterForm) -> User:
        new_user = None

        async with UnitOfWork() as uow:
            repository: UserRepository = self.repository(uow.session)

            if await repository.read_one(username=user_form.username):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail='There is already another user with this username.')

            if await repository.read_one(email=user_form.email):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail='There is already another user with this email.')

            user = user_form.model_dump()
            user['password'] = get_password_hash(user['password'])
            new_user = await repository.create(**user)

        return new_user

    async def login(self, user_form: UserLoginForm) -> User:
        email = user_form.email
        password = user_form.password

        async with UnitOfWork() as uow:
            repository: UserRepository = self.repository(uow.session)

            verified = False
            user = await repository.get_user(email)
            if user:
                verified = verify_password(
                    plain_password=password,
                    hashed_password=user.password)

            if not verified:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail='User not found or password is wrong.')

        return user
