from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    DB_HOST: str | None = None
    DB_PORT: int | None = None
    DB_USER: str | None = None
    DB_PASS: str | None = None
    DB_NAME: str | None = None
    API_KEY: str | None = None
    BOT_TOKEN: str | None = None
    ADMINS_ID: list[int] | None = None

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
