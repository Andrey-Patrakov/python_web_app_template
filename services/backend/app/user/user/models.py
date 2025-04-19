from sqlalchemy.orm import Mapped, mapped_column
from app.database.models import Base, int_pk, bool_false, created_at
from app.database.models import str_not_null, str_null, str_uniq


class User(Base):

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
