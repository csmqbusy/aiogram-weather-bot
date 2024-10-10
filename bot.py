import asyncio
from logging import basicConfig, INFO

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog import setup_dialogs

from database.orm import db_client
from handlers import admin_router, user_router
from handlers.bot_main_menu import set_main_menu
from settings.config import settings
from dialogs import all_dialogs

bot = Bot(token=settings.BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


async def main():
    basicConfig(level=INFO)
    await db_client.create_tables()
    dp.startup.register(set_main_menu)
    dp.include_router(admin_router)
    dp.include_router(user_router)
    dp.include_routers(*all_dialogs)
    setup_dialogs(dp)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
