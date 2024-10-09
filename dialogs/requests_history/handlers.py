from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager

from database.orm import db_client


async def increase_page(callback: CallbackQuery, widget: Any, dialog_manager: DialogManager):
    page = dialog_manager.dialog_data.get("history_page")
    n_of_pages = dialog_manager.dialog_data.get("n_of_history_pages")
    if page < n_of_pages:
        dialog_manager.dialog_data.update(history_page=page + 1)


async def decrease_page(callback: CallbackQuery, widget: Any, dialog_manager: DialogManager):
    page = dialog_manager.dialog_data.get("history_page")
    if page > 1:
        dialog_manager.dialog_data.update(history_page=page - 1)


async def on_report_selected(callback: CallbackQuery, widget: Any, dialog_manager: DialogManager, item_id: str):
    dialog_manager.dialog_data.update(report_id=item_id)
    await dialog_manager.next()


async def delete_request(callback: CallbackQuery, widget: Any, dialog_manager: DialogManager):
    report_id = dialog_manager.dialog_data.get("report_id")
    db_client.delete_user_report(report_id)
    await dialog_manager.back()
