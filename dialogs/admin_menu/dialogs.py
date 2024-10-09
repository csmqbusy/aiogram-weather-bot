from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Start
from aiogram_dialog.widgets.text import Const

import states
from lexicon import lexicon

admin_menu = Dialog(
    Window(
        Const(lexicon["admin_menu"]),
        Start(
            Const("Список пользователей"),
            id="users_list",
            state=states.UsersListSG.main,
            data={"userlist_page": 1}
        ),
        state=states.AdminMenuSG.main,
    )
)
