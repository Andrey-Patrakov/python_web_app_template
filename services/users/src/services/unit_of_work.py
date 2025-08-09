from database import UnitOfWork as BaseUOW
from src.repositories.users import UserRepository
from src.repositories.tokens import TokenRepository


class UnitOfWork(BaseUOW):

    @property
    def users(self) -> UserRepository:
        return UserRepository(self.session)

    @property
    def tokens(self) -> TokenRepository:
        return TokenRepository(self.session)
