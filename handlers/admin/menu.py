from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from filters import IsAdmin
from keyboards.reply.admin_menu import admin_menu_kb
from lexicon import lexicon

router = Router()
router.message.filter(IsAdmin())


@router.message(Command(commands="admin_menu"))
async def admin_panel(message: Message):
    markup = admin_menu_kb()
    await message.answer(
        text=lexicon["admin_menu"],
        reply_markup=markup
    )
