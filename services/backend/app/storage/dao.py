from sqlalchemy import select, func
from app.database import BaseDAO, Session
from .models import File


class FileDAO(BaseDAO):
    model = File

    @classmethod
    async def used_space(cls, user_id):
        async with Session() as session:
            query = select(func.sum(cls.model.size)).filter_by(user_id=user_id)
            result = (await session.execute(query)).scalar_one_or_none()
            if not result:
                return 0

            return int(result / 1024**2)
