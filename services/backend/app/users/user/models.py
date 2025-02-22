from sqlalchemy.orm import Mapped
from app.database.models import Base, int_pk, bool_true, created_at
from app.database.models import str_not_null, str_uniq


class User(Base):

    id: Mapped[int_pk]
    email: Mapped[str_uniq]
    username: Mapped[str_uniq]
    password: Mapped[str_not_null]
    is_active: Mapped[bool_true]
    created_at: Mapped[created_at]
