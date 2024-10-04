from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup

from filters import IsAdmin

router = Router()
router.message.filter(IsAdmin())


@router.message(Command(commands="admin_menu"))
async def admin_panel(message: Message):
    btn1 = KeyboardButton(text="Список пользователей")
    text = "Меню админа"
    markup = ReplyKeyboardMarkup(keyboard=[[btn1]])
    await message.answer(
        text=text,
        reply_markup=markup
    )
