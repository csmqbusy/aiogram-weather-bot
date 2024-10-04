from logging import basicConfig, INFO

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from database.orm import db_client
from handlers import admin_routers, user_routers
from settings.config import settings

bot = Bot(token=settings.BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

if __name__ == '__main__':
    basicConfig(level=INFO)
    db_client.create_tables()
    dp.include_routers(*admin_routers)
    dp.include_routers(*user_routers)
    dp.run_polling(bot, skip_updates=True)
