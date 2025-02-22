from sqlalchemy.orm import Mapped
from app.database.models import Base, int_pk, str_uniq, created_at


class BlacklistedToken(Base):
    __tablename__ = 'blacklisted_tokens'

    id: Mapped[int_pk]
    token: Mapped[str_uniq]
    blacklisted_at: Mapped[created_at]
