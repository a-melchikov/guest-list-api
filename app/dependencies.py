from typing import Annotated
from fastapi import Depends

from app.services import GuestListService, TableService
from app.repositories import GuestListRepository, TableRepository


async def guest_lists_service():
    return GuestListService(GuestListRepository)


async def tables_service():
    return TableService(TableRepository)


guest_lists_service_dependency = Annotated[
    GuestListService,
    Depends(guest_lists_service),
]

tables_service_dependency = Annotated[
    TableService,
    Depends(tables_service),
]
