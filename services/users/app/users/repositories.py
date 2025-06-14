from sqlalchemy import select, or_
from database import SQLAlchemyRepository
from .models import User


class UserRepository(SQLAlchemyRepository):
    model = User

    async def get_user(self, email_or_username: str) -> User:
        query = (
            select(self.model)
            .filter(or_(
                self.model.email == email_or_username,
                self.model.username == email_or_username)))

        return await self.session.execute(query)
