from database import BaseDBModel
from database.models import int_pk, str_uniq, str_null, str_not_null
from database.models import bool_false, created_at
from sqlalchemy.orm import Mapped, mapped_column


class User(BaseDBModel):

    id: Mapped[int_pk]
    email: Mapped[str_uniq]
    username: Mapped[str_uniq]
    password: Mapped[str_not_null]
    description: Mapped[str_null]
    is_verified: Mapped[bool_false]
    created_at: Mapped[created_at]
    avatar: Mapped[str_null]
    available_space: Mapped[int] = mapped_column(
        server_default=str(2*1024))
