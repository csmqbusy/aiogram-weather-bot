import sys
print(sys.path)
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog import setup_dialogs

from bot.database.orm import db_client
from bot.handlers import admin_router, user_router
from bot.services.set_commands import set_commands
from bot.settings.config import settings
from bot.dialogs import all_dialogs

bot = Bot(token=settings.BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


async def main():
    logging.basicConfig(level=logging.INFO)
    await db_client.create_tables()
    dp.startup.register(set_commands)
    dp.include_routers(admin_router, user_router, *all_dialogs)
    setup_dialogs(dp)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
