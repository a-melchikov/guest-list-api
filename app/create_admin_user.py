import asyncio

from passlib.context import CryptContext
from sqlalchemy import select

from app.database import async_session_maker
from app.models import User
from .config import settings
from .logger_config import get_logger

logger = get_logger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ADMIN_NAME = settings.ADMIN_NAME
ADMIN_PASSWORD = settings.ADMIN_PASSWORD


async def create_admin_user():
    async with async_session_maker() as session:
        result = await session.execute(select(User).filter_by(username=ADMIN_NAME))
        admin_user = result.scalar_one_or_none()

        if admin_user:
            logger.info("Админ-пользователь уже существует.")
            return

        hashed_password = pwd_context.hash(ADMIN_PASSWORD)
        new_admin = User(
            username="admin", hashed_password=hashed_password, is_admin=True
        )

        session.add(new_admin)
        await session.commit()
        logger.info(f"Админ-пользователь {new_admin.username} создан.")


if __name__ == "__main__":
    asyncio.run(create_admin_user())
