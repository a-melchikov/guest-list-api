from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.logger_config import get_logger

logger = get_logger(__name__)

BASE_DIR = Path(__file__).parent
ENV_FILE_PATH = BASE_DIR / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_FILE_PATH,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_ECHO: bool
    ADMIN_NAME: str
    ADMIN_PASSWORD: str
    SECRET_KEY: str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        logger.info("Настройки успешно загружены:")
        logger.info(self.model_dump())

    def get_db_url(self):
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


settings = Settings()

if __name__ == "__main__":
    print(ENV_FILE_PATH)
    print(settings.model_dump())
    print(settings.get_db_url())
