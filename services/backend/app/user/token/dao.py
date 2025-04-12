from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from .models import Token
from app.database import BaseDAO, Session


class TokenDAO(BaseDAO):
    model = Token

    @classmethod
    async def add_token(cls, user_id, token, expires_at, token_type):
        async with Session() as session:
            query = select(cls.model).filter_by(token=token)
            result = await session.execute(query)
            result = result.scalar_one_or_none()
            if result:
                return result

            new_instance = cls.model(
                user_id=user_id,
                token=token,
                expires_at=expires_at,
                token_type=token_type)

            session.add(new_instance)
            try:
                await session.commit()
            except SQLAlchemyError as e:
                await session.rollback()
                raise e

            return new_instance
