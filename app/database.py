from typing import Any
from datetime import datetime

from sqlalchemy import Integer, func
from sqlalchemy.orm import (
    DeclarativeBase,
    declared_attr,
    Mapped,
    mapped_column,
    class_mapper,
)
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    async_sessionmaker,
    create_async_engine,
)

from app.config import settings
from app.logger_config import get_logger

logger = get_logger(__name__)

DATABASE_URL = settings.get_db_url()

engine = create_async_engine(
    url=DATABASE_URL,
    echo=settings.DB_ECHO,
)
async_session_maker = async_sessionmaker(
    engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        index=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
    )

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + "s"


def connection(method):
    async def wrapper(*args, **kwargs):
        async with async_session_maker() as session:
            try:
                return await method(*args, session=session, **kwargs)
            except Exception as e:
                await session.rollback()
                logger.error(f"Ошибка в методе {method.__name__}: {e}")
                raise e
            finally:
                await session.close()

    return wrapper


def to_dict(self) -> dict[Any, Any]:
    """Универсальный метод для конвертации объекта SQLAlchemy в словарь"""
    columns = class_mapper(self.__class__).columns
    return {column.key: getattr(self, column.key) for column in columns}
