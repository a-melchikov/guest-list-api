from app.repositories import GuestListRepository
from app.schemas import GuestListUpdateSchema, GuestListResponseSchema
from app.schemas.guest_lists import GuestListCreateSchema
from .base import BaseService


class GuestListService(BaseService):
    def __init__(self, guest_list_repo: GuestListRepository) -> None:
        super().__init__(guest_list_repo)

    async def create_one_guest(
        self,
        table_data: GuestListCreateSchema,
    ) -> int:
        guest_id = await self.repo.add_one(**table_data.model_dump())
        return guest_id

    async def get_all_guests(
        self,
        name: str | None = None,
        is_present: bool | None = None,
    ) -> list[GuestListResponseSchema]:
        guests = await self.repo.get_guest_lists(name=name, is_present=is_present)
        return guests

    async def get_guest(
        self,
        guest_id: int,
    ) -> GuestListResponseSchema | None:
        guest = await self.repo.get_guest_by_id(guest_id)
        return guest

    async def update_guest(
        self,
        guest_id: int,
        guest_data: GuestListUpdateSchema,
    ) -> GuestListResponseSchema | None:
        updated_guest = await self.repo.update_guest(
            guest_id, guest_data.model_dump(exclude_unset=True)
        )
        return updated_guest
