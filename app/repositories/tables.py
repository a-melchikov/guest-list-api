from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from .base import SQLAlchemyRepository
from app.models import Table


class TableRepository(SQLAlchemyRepository):
    model = Table

    @classmethod
    async def get_tables(
        cls,
        session: AsyncSession,
        num: int | None = None,
    ):
        """
        Получение списка столов с фильтрацией по номеру стола.
        """
        query = select(cls.model)
        if num is not None:
            query = query.filter(cls.model.num == num)
        result = await session.execute(query)
        records = result.scalars().all()
        return records

    @classmethod
    async def get_table_by_id(
        cls,
        session: AsyncSession,
        table_id: int,
    ):
        """
        Получение информации о столе по id.
        """
        query = select(cls.model).filter_by(id=table_id)
        result = await session.execute(query)
        table_info = result.scalar_one_or_none()
        return table_info

    @classmethod
    async def update_table(
        cls,
        session: AsyncSession,
        table_id: int,
        values: dict,
    ):
        """
        Обновление информации о столе.
        """
        table = await cls.find_one_or_none(session, id=table_id)
        if table:
            for key, value in values.items():
                setattr(table, key, value)
            await session.commit()
        return table

    @classmethod
    async def get_guests_by_table_id(
        cls,
        session: AsyncSession,
        table_id: int,
    ):
        """
        Получение гостей за столом по table_id.
        """
        query = (
            select(cls.model)
            .filter_by(id=table_id)
            .options(selectinload(cls.model.guests))
        )
        result = await session.execute(query)
        table = result.scalar_one_or_none()
        return table.guests if table else None

    @classmethod
    async def get_tables_stats(cls, session: AsyncSession):
        """
        Получение статистики по каждому столу.
        """
        query = select(
            cls.model.id,
            cls.model.num,
            cls.model.max_guests,
            cls.model.guests_def.label("booking"),
            cls.model.guests_now.label("guestIsPresent"),
        )
        result = await session.execute(query)
        records = result.all()
        return records
