from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager


async def on_user_selected(callback: CallbackQuery, widget: Any,
                           manager: DialogManager, item_id: str):
    pass


async def decrease_page(callback: CallbackQuery, widget: Any, dialog_manager: DialogManager):
    page = dialog_manager.start_data.get("page")
    if page > 0:
        dialog_manager.start_data.update(page=page - 1)


async def increase_page(callback: CallbackQuery, widget: Any, dialog_manager: DialogManager):
    page = dialog_manager.start_data.get("page")
    n_of_pages = dialog_manager.start_data.get("n_of_pages")
    if page + 1 < n_of_pages:
        dialog_manager.start_data.update(page=page + 1)
