import secrets
from datetime import datetime, timedelta

from src.schemas.tokens import TokenSchema, TokenTypes
from src.services.unit_of_work import UnitOfWork
from src.models.tokens import Token


class TokenService:

    async def create(
            self,
            user_id: int,
            expires_delta: timedelta | None = None,
            token_type: TokenTypes = TokenTypes.BASE) -> Token:

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
            token_type: TokenTypes = TokenTypes.BASE) -> Token:

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

    async def delete(self, token: str) -> int:
        async with UnitOfWork() as uow:
            return await uow.tokens.delete(token=token)

    async def exists(
            self, token_str: str, token_type: TokenTypes = None) -> bool:
        token = await self.get(token_str, token_type)
        if token:
            return True

        return False

    async def get(
            self, token_str: str, token_type: TokenTypes = None) -> Token:
        filter_ = {"token": token_str}
        if token_type:
            filter_["token_type"] = token_type

        async with UnitOfWork() as uow:
            return await uow.tokens.read_one(**filter_)

    async def clear_dead(self):
        async with UnitOfWork() as uow:
            return await uow.tokens.clear_dead()
