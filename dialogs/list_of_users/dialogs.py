import operator

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button, Column, Select, Row, Cancel
from aiogram_dialog.widgets.text import Const, Format

import states
from lexicon import lexicon
from .getters import get_users_data
from .handlers import decrease_page, increase_page, on_user_selected

user_list = Dialog(
    Window(
        Const(lexicon["all_bot_users"]),
        Column(
            Select(
                Format(lexicon["user_format"]),
                id="s_users",
                item_id_getter=operator.itemgetter(0),
                items="users",
                on_click=on_user_selected,
            )
        ),
        Row(
            Button(Const(lexicon["back"]), id="back", on_click=decrease_page),
            Button(Format("[{page}/{n_of_pages}]"), id="current"),
            Button(Const(lexicon["forward"]), id="next", on_click=increase_page)
        ),
        Cancel(Const(lexicon["to_main_menu"]), id="button_cancel"),
        getter=get_users_data,
        state=states.UsersListSG.main,
    )
)
