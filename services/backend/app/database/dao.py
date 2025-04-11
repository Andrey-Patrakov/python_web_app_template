from sqlalchemy import update, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from .session import Session


class BaseDAO:

    @classmethod
    async def find_all(cls, **filter_by):
        async with Session() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def find_one_or_none_by_id(cls, data_id: int):
        async with Session() as session:
            query = select(cls.model).filter_by(id=data_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with Session() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def add(cls, **values):
        async with Session() as session:
            async with session.begin():
                new_instance = cls.model(**values)
                session.add(new_instance)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e

                return new_instance

    @classmethod
    async def update(cls, filter_by, **values):
        async with Session() as session:
            async with session.begin():
                where = [
                    getattr(cls.model, k) == v for k, v in filter_by.items()]
                query = (
                    update(cls.model)
                    .where(*where)
                    .values(**values)
                    .execution_options(synchronize_session='fetch')
                )
                result = await session.execute(query)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e

                return result.rowcount

    @classmethod
    async def delete(cls, delete_all: bool = False, where=None, **filter_by):
        if not delete_all and not filter_by and where is None:
            raise ValueError(
                'Необходимо указать хотя бы один параметр для удаления')

        async with Session() as session:
            async with session.begin():
                query = delete(cls.model)

                if where is not None:
                    query = query.where(where)

                query = query.filter_by(**filter_by)
                result = await session.execute(query)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e

                return result.rowcount
