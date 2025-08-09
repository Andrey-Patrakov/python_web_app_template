from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


from database import BaseDBModel
from database.models import int_pk, str_uniq, str_null, str_not_null
from database.models import bool_false, created_at, datetime_null


class User(BaseDBModel):

    id: Mapped[int_pk]
    email: Mapped[str_uniq]
    username: Mapped[str_uniq]
    password: Mapped[str_not_null]
    description: Mapped[str_null]
    is_verified: Mapped[bool_false]
    created_at: Mapped[created_at]
    avatar: Mapped[str_null]


class Token(BaseDBModel):
    id: Mapped[int_pk]
    token: Mapped[str_uniq]
    expires_at: Mapped[datetime_null]

    token_type: Mapped[int] = mapped_column(
        nullable=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id'),
        nullable=True)
