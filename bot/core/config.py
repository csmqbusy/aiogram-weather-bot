from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env.dev")

    MODE: Literal["TEST", "DEV", "PROD"] = "DEV"

    DB_HOST: str = ""
    DB_PORT: int = 5432
    DB_USER: str = ""
    DB_PASS: str = ""
    DB_NAME: str = ""

    TEST_DB_HOST: str = ""
    TEST_DB_NAME: str = ""

    REDIS_HOST: str = ""
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0

    API_KEY: str = ""

    BOT_TOKEN: str = ""
    ADMINS_ID: list[int] = Field(default_factory=list)

    @property
    def DATABASE_URL(self) -> str:
        config = (f"{self.DB_USER}:{self.DB_PASS}@"
                  f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}")
        return f"postgresql+psycopg://{config}"

    @property
    def TEST_DATABASE_URL(self) -> str:
        config = (f"{self.DB_USER}:{self.DB_PASS}@"
                  f"{self.TEST_DB_HOST}:{self.DB_PORT}/{self.TEST_DB_NAME}")
        return f"postgresql+psycopg://{config}"


settings = Settings()
