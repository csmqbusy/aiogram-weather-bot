from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager

from bot import states
from bot.database.orm import db_client
from bot.lexicon import lexicon

router = Router()


@router.message(Command(commands="start"))
async def start_cmd(message: Message) -> None:
    if message.from_user:
        await db_client.add_user(message.from_user.id)
        text = lexicon["/start"].format(message.from_user.first_name)
        await message.answer(text=text)


@router.message(Command(commands="menu"))
async def menu_cmd(message: Message, dialog_manager: DialogManager) -> None:
    await dialog_manager.start(state=states.UserMenuSG.main)
