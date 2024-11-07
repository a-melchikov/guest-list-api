from pydantic import BaseModel, ConfigDict, HttpUrl
from .tables import TableResponseSchema


class GuestListBaseSchema(BaseModel):
    name: str
    is_present: bool | None = None


class GuestListCreateSchema(GuestListBaseSchema):
    table_id: int


class GuestListUpdateSchema(BaseModel):
    name: str | None = None
    is_present: bool | None = None
    tables: HttpUrl | None = None


class GuestListResponseSchema(BaseModel):
    id: int
    name: str
    is_present: bool
    tables: TableResponseSchema

    model_config = ConfigDict(from_attributes=True)
