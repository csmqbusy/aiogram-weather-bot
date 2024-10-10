from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager

import states
from database.orm import db_client
from lexicon import lexicon

router = Router()


@router.message(Command(commands="start"))
async def start_cmd(message: Message):
    await db_client.add_user(message.from_user.id)
    text = lexicon["/start"].format(message.from_user.first_name)
    await message.answer(text=text)


@router.message(Command(commands="menu"))
async def menu_cmd(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(state=states.UserMenuSG.main)
