from .models import User
from sqlalchemy import select, or_
from app.database import Session, BaseDAO


class UsersDAO(BaseDAO):
    model = User

    @classmethod
    async def get_user_by_email(cls, email: str):
        async with Session() as session:
            query = (
                select(User)
                .filter(or_(User.email == email,
                            User.username == email)))

            result = await session.execute(query)
            return result.scalar_one_or_none()
