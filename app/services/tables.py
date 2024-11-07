from app.repositories import TableRepository
from app.schemas import (
    TableUpdateSchema,
    TableResponseSchema,
    TableStatsResponseSchema,
    GuestListResponseSchema,
)
from app.schemas.tables import TableCreateSchema
from app.services.base import BaseService


class TableService(BaseService):
    def __init__(self, table_repo: TableRepository) -> None:
        super().__init__(table_repo)

    async def create_one_table(
        self,
        table_data: TableCreateSchema,
    ) -> int:
        table_id = await self.repo.add_one(**table_data.model_dump())
        return table_id

    async def get_all_tables(
        self,
        num: int | None = None,
        nums: list[int] | None = None,
    ) -> list[TableResponseSchema]:
        tables = await self.repo.get_tables(num=num, nums=nums)
        return tables

    async def get_table(
        self,
        table_id: int,
    ) -> TableResponseSchema | None:
        table = await self.repo.get_table_by_id(table_id)
        return table

    async def update_table(
        self,
        table_id: int,
        table_data: TableUpdateSchema,
    ) -> TableResponseSchema | None:
        updated_table = await self.repo.update_table(
            table_id, table_data.model_dump(exclude_unset=True)
        )
        return updated_table

    async def get_guests_by_table_id(
        self,
        table_id: int,
        num: int | None = None,
        nums: list[int] | None = None,
    ) -> list[GuestListResponseSchema] | None:
        tables = await self.repo.get_guests_by_table_id(table_id, num, nums)
        return tables

    async def get_table_stats(
        self,
        num: int | None = None,
        nums: list[int] | None = None,
    ) -> list[TableStatsResponseSchema]:
        stats = await self.repo.get_tables_stats(num=num, nums=nums)
        return stats
