from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from guest_lists import GuestList


class Table(Base):
    num: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str | None] = mapped_column(String(255))
    max_guests: Mapped[int | None] = mapped_column(Integer)
    guests_def: Mapped[int | None] = mapped_column(Integer, default=0)
    guests_now: Mapped[int | None] = mapped_column(Integer, default=0)

    # Связь с гостями (один-ко-многим)
    guests: Mapped[list[GuestList]] = relationship(
        back_populates="table",
        cascade="all, delete-orphan",
    )

    def __str__(self) -> str:
        return (
            f"Table(id={self.id}, num={self.num}, description={self.description}, "
            f"max_guests={self.max_guests}, guests_def={self.guests_def}, guests_now={self.guests_now})"
        )

    def __repr__(self) -> str:
        return str(self)
