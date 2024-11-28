import pytest

from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog import setup_dialogs

from bot.handlers import admin_router, user_router
from bot.dialogs import all_dialogs
from bot.settings.config import settings
from bot.tests.mocked_aiogram import MockedBot, MockedSession
from bot.database.database import async_engine
from bot.database.models import Base


@pytest.fixture(scope="session")
def dp() -> Dispatcher:
    dispatcher = Dispatcher(storage=MemoryStorage())
    dispatcher.include_routers(admin_router, user_router, *all_dialogs)
    setup_dialogs(dispatcher)
    return dispatcher


@pytest.fixture(scope="session")
def bot() -> MockedBot:
    bot = MockedBot()
    bot.session = MockedSession()
    return bot


@pytest.fixture(scope="session", autouse=True)
async def prepare_test_database():
    assert settings.MODE == "TEST"

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
