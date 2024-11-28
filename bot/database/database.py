from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from bot.settings.config import settings


if settings.MODE == "TEST":
    DATABASE_URL = settings.TEST_DATABASE_URL
else:
    DATABASE_URL = settings.DATABASE_URL

async_engine = create_async_engine(
    url=DATABASE_URL, echo=False
)

async_session_factory = async_sessionmaker(async_engine)


class Base(DeclarativeBase):
    pass
