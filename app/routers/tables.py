from fastapi import APIRouter, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from pydantic import ValidationError

from app.schemas import (
    TableResponseSchema,
    TableUpdateSchema,
    GuestListResponseSchema,
    TableStatsResponseSchema,
    TableCreateSchema,
    ErrorResponseSchema,
)
from app.dependencies import tables_service_dependency

router = APIRouter()


@router.post("/", response_model=int, responses={400: {"model": ErrorResponseSchema}})
async def create_table(
    service: tables_service_dependency,
    table_data: TableCreateSchema,
) -> int:
    """
    Создать новый стол.
    """
    try:
        table_id = await service.create_one_table(table_data)
        return table_id
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Не удается создать стол: уже есть такой номер стола",
        )
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Ошибка валидации данных стола: {str(e)}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Произошла внутренняя ошибка сервера: {str(e)}",
        )


@router.get(
    "/",
    response_model=list[TableResponseSchema],
    responses={404: {"model": ErrorResponseSchema}},
)
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
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Столы не найдены"
        )
    return tables


@router.get(
    "/stats",
    response_model=list[TableStatsResponseSchema],
    responses={404: {"model": ErrorResponseSchema}},
)
async def get_table_stats(
    service: tables_service_dependency,
    num: int | None = None,
    nums: list[int] | None = Query(default=None, alias="num[]"),
) -> list[TableStatsResponseSchema]:
    """
    Получить статистику по столам.
    """
    stats = await service.get_table_stats(num=num, nums=nums)
    if not stats:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Статистика по столам не найдена",
        )
    return stats


@router.get(
    "/{table_id}",
    response_model=TableResponseSchema,
    responses={404: {"model": ErrorResponseSchema}},
)
async def get_table_by_id(
    service: tables_service_dependency,
    table_id: int,
) -> TableResponseSchema:
    """
    Получить информацию о столе по ID.
    """
    table = await service.get_table(table_id)
    if not table:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Стол не найден"
        )
    return table


@router.patch(
    "/{table_id}",
    response_model=TableResponseSchema,
    responses={
        400: {"model": ErrorResponseSchema},
        404: {"model": ErrorResponseSchema},
        422: {"model": ErrorResponseSchema},
    },
)
async def update_table(
    service: tables_service_dependency,
    table_id: int,
    table_data: TableUpdateSchema,
) -> TableResponseSchema:
    """
    Обновить информацию о столе по ID.
    """
    try:
        table = await service.update_table(table_id, table_data)
        if not table:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Стол не найден"
            )
        return table
    except IntegrityError as e:
        if "unique constraint" in str(e.orig):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Не удается обновить стол: уже существует стол с таким номером",
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Не удается обновить стол: максимальное количество гостей должно быть больше",
            )
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Ошибка валидации данных стола: {str(e)}",
        )


@router.get(
    "/{table_id}/guests",
    response_model=list[GuestListResponseSchema],
    responses={404: {"model": ErrorResponseSchema}},
)
async def get_guests_by_table_id(
    service: tables_service_dependency,
    table_id: int,
    num: int | None = None,
    nums: list[int] | None = Query(default=None, alias="num[]"),
) -> list[GuestListResponseSchema]:
    """
    Получить список гостей для стола по его table_id.
    """
    guests = await service.get_guests_by_table_id(table_id=table_id, num=num, nums=nums)
    if not guests:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Гости не найдены для данного стола",
        )
    return guests
