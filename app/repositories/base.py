from abc import ABC, abstractclassmethod
import typing
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession


class AbstractRepository(ABC):
    @abstractclassmethod
    async def add_one(cls, session: AsyncSession, **values: dict[str, typing.Any]):
        """Добавляет один экземпляр модели."""
        raise NotImplementedError

    @abstractclassmethod
    async def add_many(
        cls, session: AsyncSession, instances: list[dict[str, typing.Any]]
    ):
        """Добавляет несколько экземпляров модели."""
        raise NotImplementedError

    @abstractclassmethod
    async def patch_one(cls, session: AsyncSession, instance_id: int, **values):
        """Обновляет один экземпляр модели."""
        raise NotImplementedError

    @abstractclassmethod
    async def find_one_or_none(cls, session: AsyncSession, **filter_by):
        """Находит один экземпляр модели или возвращает None."""
        raise NotImplementedError

    @abstractclassmethod
    async def find_all(cls, session: AsyncSession, **filter_by):
        """Находит все экземпляры модели, соответствующие фильтру."""
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    @classmethod
    async def add_one(cls, session: AsyncSession, **values: dict[str, typing.Any]):
        new_instance = cls.model(**values)
        session.add(new_instance)
        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        return new_instance

    @classmethod
    async def add_many(
        cls, session: AsyncSession, instances: list[dict[str, typing.Any]]
    ):
        new_instances = [cls.model(**values) for values in instances]
        session.add_all(new_instances)
        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        return new_instances

    @classmethod
    async def patch_one(
        cls, session: AsyncSession, instance_id: int, **values: dict[str, typing.Any]
    ):
        query = select(cls.model).filter_by(id=instance_id)
        result = await session.execute(query)
        instance = result.scalar_one_or_none()

        if instance is None:
            return None

        for key, value in values.items():
            setattr(instance, key, value)

        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        return instance

    @classmethod
    async def find_one_or_none(cls, session: AsyncSession, **filter_by):
        query = select(cls.model).filter_by(**filter_by)
        result = await session.execute(query)
        record = result.scalar_one_or_none()
        return record

    @classmethod
    async def find_all(cls, session: AsyncSession, **filter_by):
        query = select(cls.model).filter_by(**filter_by)
        result = await session.execute(query)
        records = result.scalars().all()
        return records