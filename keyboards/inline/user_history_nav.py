from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from callbacks.callback_factory import ReportsActionsCb, ReportViewCb


def reports_history_kb(
        reports: list,
        slice_: slice,
        curr_page_text: str,
        prev: bool = False,
        next_: bool = False
) -> InlineKeyboardMarkup:

    report_buttons = []
    for report in reports[slice_]:
        report_buttons.append(
            [
                InlineKeyboardButton(
                    text=f"{report.city} {report.date.day}.{report.date.month}.{report.date.year}",
                    callback_data=ReportViewCb(action="show", report_id=report.id).pack()
                )
            ]
        )
    button_page = InlineKeyboardButton(
        text=curr_page_text,
        callback_data=ReportsActionsCb(action="None").pack()
    )
    button_next = InlineKeyboardButton(
        text="Вперед",
        callback_data=ReportsActionsCb(action="next").pack()
    )
    button_prev = InlineKeyboardButton(
        text="Назад",
        callback_data=ReportsActionsCb(action="prev").pack()
    )

    if next_ and prev:
        buttons = [*report_buttons, [button_prev, button_page, button_next]]
    elif next_:
        buttons = [*report_buttons, [button_page, button_next]]
    else:
        buttons = [*report_buttons, [button_prev, button_page]]

    markup = InlineKeyboardMarkup(
        inline_keyboard=buttons
    )

    return markup
