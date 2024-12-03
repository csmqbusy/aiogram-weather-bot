import pytest

from bot.core.config import settings
from bot.database.database import async_engine
from bot.database.models import Base


@pytest.fixture(scope="function", autouse=True)
async def prepare_test_database():
    assert settings.MODE == "TEST"

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
