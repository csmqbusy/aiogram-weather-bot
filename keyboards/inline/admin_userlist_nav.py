from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from callbacks import AdminsActionsCb
from lexicon import lexicon


def userlist_kb(
        users: list,
        slice_: slice,
        curr_page_text: str,
        prev: bool = False,
        next_: bool = False
) -> InlineKeyboardMarkup:

    user_buttons = []
    for user in users[slice_]:
        conn_date = f"{user.connection_date.day}.{user.connection_date.month}.{user.connection_date.year}"
        user_buttons.append(
            [
                InlineKeyboardButton(
                    text=lexicon["user_format"].format(user.id, user.tg_id, conn_date, len(user.reports)),
                    callback_data=AdminsActionsCb(action="None").pack()
                )
            ]
        )
    button_page = InlineKeyboardButton(
        text=curr_page_text,
        callback_data=AdminsActionsCb(action="None").pack()
    )
    button_prev = InlineKeyboardButton(
        text=lexicon["back"],
        callback_data=AdminsActionsCb(action="prev_users_page").pack()
    )
    button_next = InlineKeyboardButton(
        text=lexicon["forward"],
        callback_data=AdminsActionsCb(action="next_users_page").pack()
    )

    if next_ and prev:
        buttons = [*user_buttons, [button_prev, button_page, button_next]]
    elif next_:
        buttons = [*user_buttons, [button_page, button_next]]
    else:
        buttons = [*user_buttons, [button_prev, button_page]]

    markup = InlineKeyboardMarkup(
        inline_keyboard=buttons
    )

    return markup
