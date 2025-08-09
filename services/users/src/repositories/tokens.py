from sqlalchemy import delete
from datetime import datetime

from database import SQLAlchemyRepository
from src.models.tokens import Token


class TokenRepository(SQLAlchemyRepository):
    model = Token

    async def clear_dead(self, token_type: int | None = None):
        now = datetime.now()
        filter_ = {'token_type': token_type} if token_type else {}

        query = (
            delete(self.model)
            .filter(filter_)
            .where(self.model.expires_at < now))

        return await self.session.execute(query)
