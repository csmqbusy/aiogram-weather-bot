from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from database.orm import db_client
from keyboards.reply.user_menu import user_menu_kb

router = Router()


@router.message(Command(commands="start"))
async def start_cmd(message: Message):
    db_client.add_user(message.from_user.id)
    markup = user_menu_kb()
    text = f"Привет, {message.from_user.first_name}! Я бот, который расскажет тебе о погоде на сегодня"
    await message.answer(
        text=text,
        reply_markup=markup
    )


@router.message(Command(commands="menu"))
async def menu_cmd(message: Message):
    markup = user_menu_kb()
    text = "Главное меню"
    await message.answer(
        text=text,
        reply_markup=markup
    )
