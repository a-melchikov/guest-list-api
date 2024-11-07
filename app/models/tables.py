from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import String, Integer, select, func
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from app.database import Base, async_session_maker
from .guest_lists import GuestList

if TYPE_CHECKING:
    from guest_lists import GuestList


class Table(Base):
    num: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str | None] = mapped_column(String(255))
    max_guests: Mapped[int | None] = mapped_column(Integer)

    # Связь с гостями (один-ко-многим)
    guests: Mapped[list[GuestList]] = relationship(
        back_populates="table",
        cascade="all, delete-orphan",
    )

    @validates("guests")
    def validate_guests_def(self, key, guests):
        if self.max_guests is not None and len(guests) > self.max_guests:
            raise ValueError(
                f"Количество гостей ({len(guests)}) не может превышать максимальное значение ({self.max_guests})."
            )
        return guests

    @property
    async def guests_def(self):
        """
        Возвращает количество гостей, которых ожидают за столом.
        """
        async with async_session_maker() as session:
            query = (
                select(func.count())
                .select_from(GuestList)
                .where(GuestList.table_id == self.id)
            )
            result = await session.execute(query)
            guests_def = result.scalar_one_or_none()
            return guests_def or 0

    @property
    async def guests_now(self):
        """
        Возвращает количество гостей, которые сейчас за столом.
        """
        async with async_session_maker() as session:
            query = (
                select(func.count())
                .select_from(GuestList)
                .where(GuestList.table_id == self.id, GuestList.is_present.is_(True))
            )
            result = await session.execute(query)
            guests_now = result.scalar_one_or_none()
            return guests_now or 0

    def __str__(self) -> str:
        return (
            f"Table(id={self.id}, num={self.num}, description={self.description}, "
            f"max_guests={self.max_guests}, guests_def={self.guests_def}, guests_now={self.guests_now})"
        )

    def __repr__(self) -> str:
        return str(self)
