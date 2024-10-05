from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from callbacks import ReportViewCb
from lexicon import lexicon


def report_view_kb(report_id: int) -> InlineKeyboardMarkup:
    button_back = InlineKeyboardButton(
        text=lexicon["back"],
        callback_data="back_to_history"
    )
    button_delete = InlineKeyboardButton(
        text=lexicon["delete_request"],
        callback_data=ReportViewCb(action="delete", report_id=report_id).pack()
    )
    markup = InlineKeyboardMarkup(
        inline_keyboard=[[button_back], [button_delete]]
    )

    return markup
