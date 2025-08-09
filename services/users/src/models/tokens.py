from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


from database import BaseDBModel
from database.models import int_pk, str_uniq
from database.models import datetime_null


class Token(BaseDBModel):
    id: Mapped[int_pk]
    token: Mapped[str_uniq]
    expires_at: Mapped[datetime_null]

    token_type: Mapped[int] = mapped_column(
        nullable=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id'),
        nullable=True)
