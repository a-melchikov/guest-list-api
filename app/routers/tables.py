from fastapi import APIRouter, HTTPException, Query

from app.schemas import (
    TableResponseSchema,
    TableUpdateSchema,
    GuestListResponseSchema,
    TableStatsResponseSchema,
    TableCreateSchema,
)
from app.dependencies import tables_service_dependency

router = APIRouter()


@router.post("/", response_model=int)
async def create_table(
    service: tables_service_dependency,
    table_data: TableCreateSchema,
) -> int:
    try:
        table_id = await service.create_one_table(table_data)
        return table_id
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[TableResponseSchema])
async def get_all_tables(
    service: tables_service_dependency,
    num: int | None = None,
    nums: list[int] | None = Query(default=None, alias="num[]"),
) -> list[TableResponseSchema]:
    """
    Получить список всех столов с фильтрацией по номеру.
    """
    tables = await service.get_all_tables(num=num, nums=nums)
    if not tables:
        raise HTTPException(status_code=404, detail="Tables not found")
    return tables


@router.get("/stats", response_model=list[TableStatsResponseSchema])
async def get_table_stats(
    service: tables_service_dependency,
    num: int | None = None,
    nums: list[int] | None = Query(default=None, alias="num[]"),
) -> list[TableStatsResponseSchema]:
    """
    Получить статистику по столам.
    """
    stats = await service.get_table_stats(num=num, nums=nums)
    return stats


@router.get("/{table_id}", response_model=TableResponseSchema)
async def get_table_by_id(
    service: tables_service_dependency,
    table_id: int,
) -> TableResponseSchema:
    """
    Получить информацию о столе по ID.
    """
    table = await service.get_table(table_id)
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")
    return table


@router.patch("/{table_id}", response_model=TableResponseSchema)
async def update_table(
    service: tables_service_dependency,
    table_id: int,
    table_data: TableUpdateSchema,
) -> TableResponseSchema:
    """
    Обновить информацию о столе по ID.
    """
    table = await service.update_table(table_id, table_data)
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")
    return table


@router.get("/{table_id}/guests", response_model=list[GuestListResponseSchema])
async def get_guests_by_table_id(
    service: tables_service_dependency,
    table_id: int,
) -> list[GuestListResponseSchema]:
    """
    Получить список гостей для стола по его table_id.
    """
    guests = await service.get_guests_by_table_id(table_id=table_id)
    if guests is None:
        raise HTTPException(status_code=404, detail="No guests found for this table")
    return guests
