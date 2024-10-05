from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from database.orm import db_client
from keyboards.reply.user_menu import user_menu_kb
from lexicon import lexicon

router = Router()


@router.message(Command(commands="start"))
async def start_cmd(message: Message):
    db_client.add_user(message.from_user.id)
    markup = user_menu_kb()
    text = lexicon["/start"].format(message.from_user.first_name)
    await message.answer(
        text=text,
        reply_markup=markup
    )


@router.message(Command(commands="menu"))
async def menu_cmd(message: Message):
    markup = user_menu_kb()
    await message.answer(
        text=lexicon["main_menu_user"],
        reply_markup=markup
    )
