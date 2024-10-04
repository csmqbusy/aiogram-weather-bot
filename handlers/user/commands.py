from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup

from database.orm import db_client

router = Router()


@router.message(F.text == "Меню")
@router.message(Command(commands="start"))
async def start_cmd(message: Message):
    db_client.add_user(message.from_user.id)
    btn1 = KeyboardButton(text="Погода в моем городе")
    btn2 = KeyboardButton(text="Погода в другом месте")
    btn3 = KeyboardButton(text="История")
    btn4 = KeyboardButton(text="Установить свой город")
    markup = ReplyKeyboardMarkup(keyboard=[[btn1], [btn2], [btn3], [btn4]])
    text = f"Привет, {message.from_user.first_name}! Я бот, который расскажет тебе о погоде на сегодня"
    await message.answer(
        text=text,
        reply_markup=markup
    )
