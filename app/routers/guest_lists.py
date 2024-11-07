from fastapi import APIRouter, HTTPException, status

from app.schemas import (
    GuestListResponseSchema,
    GuestListUpdateSchema,
    GuestListCreateSchema,
)
from app.dependencies import guest_lists_service_dependency

router = APIRouter()


@router.post("/", response_model=int, status_code=status.HTTP_201_CREATED)
async def create_guest_list(
    service: guest_lists_service_dependency,
    guest_data: GuestListCreateSchema,
) -> int:
    """
    Создать новый гостевой список.
    """
    try:
        guest_list_id = await service.create_one_guest(guest_data)
        return guest_list_id
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[GuestListResponseSchema])
async def get_all_guest_lists(
    service: guest_lists_service_dependency,
    name: str | None = None,
    is_present: bool | None = None,
) -> list[GuestListResponseSchema]:
    """
    Получить список всех гостевых списков с фильтрацией по имени и статусу присутствия.
    """
    guest_lists = await service.get_all_guests(name=name, is_present=is_present)
    if not guest_lists:
        raise HTTPException(status_code=404, detail="Guest lists not found")
    return guest_lists


@router.get("/{guest_id}", response_model=GuestListResponseSchema)
async def get_guest_list_by_id(
    service: guest_lists_service_dependency,
    guest_id: int,
) -> GuestListResponseSchema:
    """
    Получить гостевой список по ID.
    """
    guest_list = await service.get_guest(guest_id)
    if not guest_list:
        raise HTTPException(status_code=404, detail="Guest list not found")
    return guest_list


@router.patch("/{guest_id}", response_model=GuestListResponseSchema)
async def update_guest_list(
    service: guest_lists_service_dependency,
    guest_id: int,
    guest_data: GuestListUpdateSchema,
) -> GuestListResponseSchema:
    """
    Обновить гостевой список по ID.
    """
    guest_list = await service.update_guest(guest_id, guest_data)
    if not guest_list:
        raise HTTPException(status_code=404, detail="Guest list not found")
    return guest_list
