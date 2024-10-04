from sqlalchemy.orm import Session, sessionmaker, DeclarativeBase
from sqlalchemy import URL, create_engine, text, String
from settings.config import settings

sync_engine = create_engine(
    url=settings.DATABASE_URL_psycopg,
    echo=True
)

session_factory = sessionmaker(sync_engine)


class Base(DeclarativeBase):
    pass
