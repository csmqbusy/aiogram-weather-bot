from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from settings.config import settings

sync_engine = create_engine(
    url=settings.DATABASE_URL_psycopg,
    echo=False
)

session_factory = sessionmaker(sync_engine)

async_engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=False
)

async_session_factory = async_sessionmaker(async_engine)


class Base(DeclarativeBase):
    pass
