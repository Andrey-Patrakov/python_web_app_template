from .models import User
from sqlalchemy import select, or_
from app.database import Session, BaseDAO


class UsersDAO(BaseDAO):
    model = User

    @classmethod
    async def get_user_by_email(cls, email: str):
        async with Session() as session:
            query = (
                select(cls.model)
                .filter(or_(cls.model.email == email,
                            cls.model.username == email)))

            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def check_user_exists(cls, email: str, username: str):
        async with Session() as session:
            query = (
                select(cls.model)
                .filter(or_(cls.model.email == email,
                            cls.model.username == username)))

            result = await session.execute(query)
            return result.scalar_one_or_none()
