from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from callbacks.callback_factory import ReportViewCb


def report_view_kb(report_id: int) -> InlineKeyboardMarkup:
    button_back = InlineKeyboardButton(
        text="Назад",
        callback_data="back_to_history"
    )
    button_delete = InlineKeyboardButton(
        text="Удалить запрос",
        callback_data=ReportViewCb(action="delete", report_id=report_id).pack()
    )
    markup = InlineKeyboardMarkup(
        inline_keyboard=[[button_back], [button_delete]]
    )

    return markup
