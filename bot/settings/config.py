from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    DB_HOST: str = ""
    DB_PORT: int = 5432
    DB_USER: str = ""
    DB_PASS: str = ""
    DB_NAME: str = ""
    API_KEY: str = ""
    BOT_TOKEN: str = ""
    ADMINS_ID: list[int] = Field(default_factory=list)

    @property
    def DATABASE_URL_psycopg(self) -> str:
        config = (f"{self.DB_USER}:{self.DB_PASS}@"
                  f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}")
        return f"postgresql+psycopg://{config}"

    @property
    def DATABASE_URL_asyncpg(self) -> str:
        config = (f"{self.DB_USER}:{self.DB_PASS}@"
                  f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}")
        return f"postgresql+asyncpg://{config}"


settings = Settings()
