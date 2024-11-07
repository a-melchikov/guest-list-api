import asyncio

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.schemas import GuestListResponseSchema, TableResponseSchema
from app.database import async_session_maker, to_dict
from app.models import GuestList, Table
from .base import SQLAlchemyRepository


class GuestListRepository(SQLAlchemyRepository):
    model = GuestList

    @classmethod
    async def get_guest_lists(
        cls,
        name: str | None = None,
        is_present: bool | None = None,
    ) -> list[GuestListResponseSchema]:
        """
        Получение списка гостей с фильтрацией по имени и статусу присутствия.
        """
        async with async_session_maker() as session:
            query = select(cls.model).options(selectinload(cls.model.table))
            if name:
                query = query.filter(cls.model.name == name)
            if is_present is not None:
                query = query.filter(cls.model.is_present == is_present)
            result = await session.execute(query)
            records = result.scalars().all()

            guest_lists = await asyncio.gather(
                *[cls.format_guest_data(guest) for guest in records]
            )
            return guest_lists

    @classmethod
    async def format_table_data(cls, table: Table) -> TableResponseSchema:
        async with async_session_maker() as session:
            query = (
                select(Table).options(selectinload(Table.guests)).filter_by(id=table.id)
            )
            result = await session.execute(query)
            table_with_guests = result.scalar_one_or_none()

            guest_links = [
                f"/api/guest_lists/{guest.id}" for guest in table_with_guests.guests
            ]

            table_data = to_dict(table_with_guests)
            table_data.update(
                {
                    "guests": guest_links,
                }
            )
            return TableResponseSchema(**table_data)

    @classmethod
    async def format_guest_data(cls, guest: GuestList) -> GuestListResponseSchema:
        guest_data = to_dict(guest)
        tables = await cls.format_table_data(guest.table)
        guest_data.update(
            {
                "tables": tables.model_dump(),
            }
        )
        del guest_data["table_id"]
        return GuestListResponseSchema(**guest_data)

    @classmethod
    async def get_guest_by_id(
        cls,
        guest_id: int,
    ) -> GuestListResponseSchema | None:
        """
        Получение гостя по id.
        """
        async with async_session_maker() as session:
            query = (
                select(cls.model)
                .options(selectinload(cls.model.table))
                .filter_by(id=guest_id)
            )
            result = await session.execute(query)
            guest_info = result.unique().scalar_one_or_none()
            return await cls.format_guest_data(guest_info) if guest_info else None

    @classmethod
    async def update_guest(
        cls,
        guest_id: int,
        values: dict[str, str | int | None],
    ) -> GuestListResponseSchema | None:
        """
        Обновление информации о госте.
        """
        async with async_session_maker() as session:
            guest = await session.execute(
                select(cls.model)
                .options(selectinload(cls.model.table))
                .filter_by(id=guest_id)
            )
            guest = guest.scalars().first()

            if guest:
                for key, value in values.items():
                    setattr(guest, key, value)
                await session.commit()

                return await cls.format_guest_data(guest)
            return None
