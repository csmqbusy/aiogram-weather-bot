import operator

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button, Column, Select, Row
from aiogram_dialog.widgets.text import Const, Format

import states
from .getters import get_users_data
from .handlers import decrease_page, increase_page, on_user_selected

user_list = Dialog(
    Window(
        Const("Привет!"),
        Column(
            Select(
                Format("{item[0]}) id: {item[1]}, подключился {item[2]}, {item[3]} отчётов"),
                id="s_users",
                item_id_getter=operator.itemgetter(0),
                items="users",
                on_click=on_user_selected,
            )
        ),
        Row(
            Button(Const("back"), id="back", on_click=decrease_page),
            Button(Format("{page}/{n_of_pages}"), id="current"),
            Button(Const("next"), id="next", on_click=increase_page)
        ),
        getter=get_users_data,
        state=states.UsersListSG.main,
    )
)
