from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from .base import SQLAlchemyRepository
from app.models import GuestList


class GuestListRepository(SQLAlchemyRepository):
    model = GuestList

    @classmethod
    async def get_guest_lists(
        cls,
        session: AsyncSession,
        name: str | None = None,
        is_present: bool | None = None,
    ):
        """
        Получение списка гостей с фильтрацией по имени и статусу присутствия.
        """
        query = select(cls.model).options(selectinload(cls.model.table))
        if name:
            query = query.filter(cls.model.name == name)
        if is_present is not None:
            query = query.filter(cls.model.is_present == is_present)
        result = await session.execute(query)
        records = result.scalars().all()
        return records

    @classmethod
    async def get_guest_by_id(
        cls,
        session: AsyncSession,
        guest_id: int,
    ):
        """
        Получение гостя по id.
        """
        query = (
            select(cls.model)
            .filter_by(id=guest_id)
            .options(selectinload(cls.model.table))
        )
        result = await session.execute(query)
        guest = result.scalar_one_or_none()
        return guest

    @classmethod
    async def update_guest(
        cls,
        session: AsyncSession,
        guest_id: int,
        values: dict,
    ):
        """
        Обновление информации о госте.
        """
        guest = await cls.find_one_or_none(session, id=guest_id)
        if guest:
            for key, value in values.items():
                setattr(guest, key, value)
            await session.commit()
        return guest
