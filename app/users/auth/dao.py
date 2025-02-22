from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from app.database import BaseDAO, Session
from .models import BlacklistedToken


class AuthDAO(BaseDAO):
    model = BlacklistedToken

    @classmethod
    async def add_token_to_blacklist(cls, token):
        async with Session() as session:
            query = select(cls.model).filter_by(token=token)
            result = await session.execute(query)
            result = result.scalar_one_or_none()
            if result:
                return result

            new_instance = cls.model(token=token)
            session.add(new_instance)
            try:
                await session.commit()
            except SQLAlchemyError as e:
                await session.rollback()
                raise e

            return new_instance
