from datetime import datetime
from typing import Annotated

from sqlalchemy import func, true, false
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, declared_attr
from sqlalchemy.orm import mapped_column

int_pk = Annotated[int, mapped_column(primary_key=True)]
str_uniq = Annotated[str, mapped_column(unique=True, nullable=False)]
str_not_null = Annotated[str, mapped_column(nullable=False)]
str_null = Annotated[str, mapped_column(nullable=True)]
bool_true = Annotated[bool, mapped_column(server_default=true())]
bool_false = Annotated[bool, mapped_column(server_default=false())]
created_at = Annotated[datetime, mapped_column(server_default=func.now())]
datetime_null = Annotated[datetime, mapped_column(nullable=True)]


# alembic init -t async migration -- Инициализация alembic
# alembic revision --autogenerate -m "Initial revision" -- сгенерировать скрипт
# alembic upgrade head -- Обновить БД
# alembic downgrade -1 -- Откатить обновление
class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f'{cls.__name__.lower()}s'
