from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager

from bot import states
from bot.filters import IsAdmin

router = Router()
router.message.filter(IsAdmin())


@router.message(Command(commands="admin_menu"))
async def admin_panel(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(state=states.AdminMenuSG.main)
