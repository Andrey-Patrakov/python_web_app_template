import secrets
from datetime import datetime, timedelta

from src.schemas.tokens import TokenSchema, TokenTypes
from src.services.unit_of_work import UnitOfWork


class TokenService:

    async def create(
            self,
            user_id: int,
            expires_delta: timedelta | None = None,
            token_type: TokenTypes = TokenTypes.BASE):

        token = secrets.token_urlsafe()
        return await self.add(
            token=token,
            user_id=user_id,
            expires_delta=expires_delta,
            token_type=token_type)

    async def add(
            self,
            token: str,
            user_id: int,
            expires_delta: timedelta | None = None,
            token_type: TokenTypes = TokenTypes.BASE):

        async with UnitOfWork() as uow:
            expires_at = None
            if expires_delta is not None:
                expires_at = datetime.now() + expires_delta

            token_data = TokenSchema(
                user_id=user_id,
                token=token,
                expires_at=expires_at,
                token_type=token_type).model_dump()

            return await uow.tokens.create(**token_data)

    async def delete(self, token: str):
        async with UnitOfWork() as uow:
            return await uow.tokens.delete(token=token)

    async def exists(self, token: str):
        async with UnitOfWork() as uow:
            return await uow.tokens.read_one(token=token)

    async def clear_dead(self):
        async with UnitOfWork() as uow:
            return await uow.tokens.clear_dead()
