from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup

from database.orm import db_client
from keyboards.reply.user_menu import user_menu_kb

router = Router()


@router.message(F.text == "Меню")
@router.message(Command(commands="start"))
async def start_cmd(message: Message):
    db_client.add_user(message.from_user.id)
    markup = user_menu_kb()
    text = f"Привет, {message.from_user.first_name}! Я бот, который расскажет тебе о погоде на сегодня"
    await message.answer(
        text=text,
        reply_markup=markup
    )
