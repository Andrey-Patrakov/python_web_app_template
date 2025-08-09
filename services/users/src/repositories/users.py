from sqlalchemy import select, or_
from database import SQLAlchemyRepository
from src.models.users import User


class UserRepository(SQLAlchemyRepository):
    model = User

    async def get_by_username(self, email_or_username: str) -> User:
        query = (
            select(self.model)
            .filter(or_(
                self.model.email == email_or_username,
                self.model.username == email_or_username)))

        result = await self.session.execute(query)
        return result.scalar_one_or_none()
