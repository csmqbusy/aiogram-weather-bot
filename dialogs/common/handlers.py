from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager


async def close_current_dialog(
        callback: CallbackQuery, widget: Any, dialog_manager: DialogManager):
    await dialog_manager.done()
