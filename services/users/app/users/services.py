from fastapi import HTTPException, status, Request, Response
from database import SQLAlchemyService, UnitOfWork

from .repositories import UserRepository
from .models import User
from .schemas import UserRegisterForm, UserLoginForm

from app.utils.password import get_password_hash, verify_password
from app.utils.jwt import AccessToken, RefreshToken
from app.utils.jwt import TokenCorruptedError, TokenExpiredError
from app.utils.jwt import TokenMissingError


TOKEN_EXCEPTIONS = (TokenCorruptedError, TokenExpiredError, TokenMissingError)


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

    async def login(
            self, user_form: UserLoginForm,
            request: Request, response: Response) -> User:

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

            token_data = {'sub': str(user.id)}
            AccessToken(request, response).generate_and_save(token_data)
            RefreshToken(request, response).generate_and_save(token_data)

        return user

    async def logout(self, request: Request, response: Response):
        try:
            AccessToken(request, response).delete()
        except Exception:
            pass

        try:
            RefreshToken(request, response).delete()
        except Exception:
            pass

    async def refresh_access_token(self, request: Request, response: Response):
        refresh_token = RefreshToken(
            request, response).read_and_decode()

        user_id = refresh_token.get('sub')

        token_data = {'sub': user_id}
        access_token = AccessToken(
            request, response).generate_and_save(token_data)

        return AccessToken(request, response).decode(access_token)

    async def get_current_user(
            self,
            request: Request, response: Response):
        unauthorized_exception = HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Unauthorized.')

        token = {}
        try:
            try:
                token = AccessToken(request, response).read_and_decode()
            except TOKEN_EXCEPTIONS:
                token = await self.refresh_access_token(request, response)

        except TOKEN_EXCEPTIONS:
            raise unauthorized_exception

        user_id = token.get('sub')
        if not user_id:
            raise unauthorized_exception

        async with UnitOfWork() as uow:
            repository: UserRepository = self.repository(uow.session)

            user = await repository.read_one(id=int(user_id))
            if not user:
                raise unauthorized_exception

            return user
