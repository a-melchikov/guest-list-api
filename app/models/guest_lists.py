from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from tables import Table


class GuestList(Base):
    __tablename__ = "guest_lists"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    is_present: Mapped[bool | None] = mapped_column(Boolean, default=False)

    # Внешний ключ и связь с таблицей Table (многие-к-одному)
    table_id: Mapped[int] = mapped_column(ForeignKey("tables.id"))
    table: Mapped[Table] = relationship(back_populates="guests")

    def __str__(self) -> str:
        return (
            f"GuestList(id={self.id}, name={self.name}, is_present={self.is_present})"
        )

    def __repr__(self) -> str:
        return str(self)
