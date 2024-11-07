import asyncio
from datetime import datetime
from sqlalchemy import Select, select
from sqlalchemy.orm import selectinload

from app.schemas import TableResponseSchema, TableStatsResponseSchema
from app.database import async_session_maker, to_dict
from app.models import Table
from app.schemas import GuestListResponseSchema
from .base import SQLAlchemyRepository


class TableRepository(SQLAlchemyRepository):
    model = Table

    @classmethod
    async def get_query_with_check_nums(
        cls,
        query: Select,
        num: int | None,
        nums: list[int] | None,
    ) -> Select:
        if isinstance(nums, list):
            if num is not None:
                nums.append(num)
                num = None
        if num is not None:
            query = query.filter(cls.model.num == num)
        if nums is not None:
            query = query.filter(cls.model.num.in_(nums))
        return query

    @classmethod
    async def get_tables(
        cls,
        num: int | None = None,
        nums: list[int] | None = None,
    ) -> list[TableResponseSchema]:
        async with async_session_maker() as session:
            query = select(cls.model).options(selectinload(cls.model.guests))
            query = await cls.get_query_with_check_nums(query, num, nums)
            result = await session.execute(query)
            records = result.scalars().all()

            tables_with_guests = await asyncio.gather(
                *[cls.format_table_data(table) for table in records]
            )
            return tables_with_guests

    @classmethod
    async def format_table_data(cls, table: Table) -> TableResponseSchema:
        table_data = to_dict(table)
        table_data.update(
            {
                "guests": [f"/api/guest_lists/{guest.id}" for guest in table.guests],
            }
        )
        return TableResponseSchema(**table_data)

    @classmethod
    async def get_table_by_id(
        cls,
        table_id: int,
    ) -> TableResponseSchema | None:
        """
        Получение информации о столе по id.
        """
        async with async_session_maker() as session:
            query = (
                select(cls.model)
                .options(selectinload(cls.model.guests))
                .filter_by(id=table_id)
            )
            result = await session.execute(query)
            table_info = result.scalar_one_or_none()
            return await cls.format_table_data(table_info) if table_info else None

    @classmethod
    async def update_table(
        cls,
        table_id: int,
        values: dict[str, str | int | None],
    ) -> TableResponseSchema | None:
        """
        Обновление информации о столе.
        """
        async with async_session_maker() as session:
            table = await session.execute(
                select(Table)
                .options(selectinload(cls.model.guests))
                .filter_by(id=table_id)
            )
            table = table.scalars().first()

            if table:
                table.updated_at = datetime.utcnow()
                for key, value in values.items():
                    setattr(table, key, value)
                await session.commit()

                return await cls.format_table_data(table)
            return None

    @classmethod
    async def get_guests_by_table_id(
        cls,
        table_id: int,
    ) -> list[GuestListResponseSchema] | None:
        """
        Получение гостей за столом по table_id с информацией о столе.
        """
        async with async_session_maker() as session:
            query = (
                select(cls.model)
                .filter_by(id=table_id)
                .options(selectinload(cls.model.guests))
            )
            result = await session.execute(query)
            table = result.scalar_one_or_none()

            if table:
                guests_data = [
                    GuestListResponseSchema(
                        id=guest.id,
                        name=guest.name,
                        is_present=guest.is_present,
                        tables=TableResponseSchema(
                            id=table.id,
                            num=table.num,
                            description=table.description,
                            max_guests=table.max_guests,
                            guests_def=table.guests_def,
                            guests_now=table.guests_now,
                            guests=[
                                f"/api/guest_lists/{guest.id}" for guest in table.guests
                            ],
                        ),
                    )
                    for guest in table.guests
                ]
                return guests_data
            return None

    @classmethod
    async def get_tables_stats(
        cls,
        num: int | None = None,
        nums: list[int] | None = None,
    ) -> list[TableStatsResponseSchema]:
        """
        Получение статистики по каждому столу.
        """
        async with async_session_maker() as session:
            query = select(cls.model).options(selectinload(cls.model.guests))
            print(num, nums)
            query = await cls.get_query_with_check_nums(query, num, nums)
            result = await session.execute(query)
            records = result.scalars().all()

            res = await asyncio.gather(
                *[cls._create_table_stats_response(record) for record in records]
            )

            return res

    @staticmethod
    async def _create_table_stats_response(record) -> TableStatsResponseSchema:
        return TableStatsResponseSchema(
            id=record.id,
            num=record.num,
            max_guests=record.max_guests,
            booking=record.guests_def,
            guest_is_present=record.guests_now,
        )


async def main():
    tables = await TableRepository.get_tables_stats()
    print(tables)


if __name__ == "__main__":
    asyncio.run(main())
