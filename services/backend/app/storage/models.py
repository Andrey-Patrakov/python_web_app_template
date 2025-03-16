from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.database.models import Base, int_pk, str_uniq


class File(Base):

    id: Mapped[int_pk]
    filename: Mapped[str]
    size: Mapped[float]
    storage_id: Mapped[str_uniq]
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id'),
        nullable=False)
