from pydantic import BaseModel, ConfigDict, constr


class TableBaseSchema(BaseModel):
    num: int
    description: str | None = None
    max_guests: int | None = None


class TableCreateSchema(TableBaseSchema):
    pass


class TableUpdateSchema(BaseModel):
    num: int | None = None
    description: str | None = None
    max_guests: int | None = None


class TableGuestListResponseSchema(BaseModel):
    id: int
    num: int
    description: str | None = None
    max_guests: int | None = None
    guests_def: int
    guests_now: int
    guests: list[constr(pattern=r"^/api/guest_lists/\d+$")]


class TableStatsResponseSchema(BaseModel):
    id: int
    num: int
    max_guests: int | None = None
    booking: int
    guest_is_present: int


class TableResponseSchema(BaseModel):
    id: int
    num: int
    description: str | None = None
    max_guests: int | None = None
    guests_def: int
    guests_now: int
    guests: list[constr(pattern=r"^/api/guest_lists/\d+$")]

    model_config = ConfigDict(from_attributes=True)
