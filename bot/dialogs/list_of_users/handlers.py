from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager


async def on_user_selected(
        callback: CallbackQuery,
        widget: Any,
        dialog_manager: DialogManager,
        item_id: str
) -> None:
    pass


async def decrease_page(
        callback: CallbackQuery,
        widget: Any,
        dialog_manager: DialogManager
) -> None:
    page = dialog_manager.dialog_data["userlist_page"]
    if page > 1:
        dialog_manager.dialog_data.update(userlist_page=page - 1)


async def increase_page(
        callback: CallbackQuery,
        widget: Any,
        dialog_manager: DialogManager
) -> None:
    page = dialog_manager.dialog_data["userlist_page"]
    n_of_pages = dialog_manager.dialog_data["n_of_users_pages"]
    if page < n_of_pages:
        dialog_manager.dialog_data.update(userlist_page=page + 1)
