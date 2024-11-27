from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager

from bot.database.orm import db_client


async def increase_page(
        callback: CallbackQuery,
        widget: Any,
        dialog_manager: DialogManager,
) -> None:
    page = dialog_manager.dialog_data["history_page"]
    n_of_pages = dialog_manager.dialog_data["n_of_history_pages"]
    if page < n_of_pages:
        dialog_manager.dialog_data.update(history_page=page + 1)


async def decrease_page(
        callback: CallbackQuery,
        widget: Any,
        dialog_manager: DialogManager,
) -> None:
    page = dialog_manager.dialog_data["history_page"]
    if page > 1:
        dialog_manager.dialog_data.update(history_page=page - 1)


async def on_report_selected(
        callback: CallbackQuery,
        widget: Any,
        dialog_manager: DialogManager,
        item_id: str
) -> None:
    report_id = int(item_id)
    dialog_manager.dialog_data.update(report_id=report_id)
    await dialog_manager.next()


async def delete_request(
        callback: CallbackQuery,
        widget: Any,
        dialog_manager: DialogManager
) -> None:
    report_id = dialog_manager.dialog_data["report_id"]
    await db_client.delete_user_report(report_id)
    await dialog_manager.back()
