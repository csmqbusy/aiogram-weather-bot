from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Start
from aiogram_dialog.widgets.text import Const

import states
from lexicon import lexicon
from dialogs.common.handlers import close_current_dialog

admin_menu = Dialog(
    Window(
        Const(lexicon["admin_menu"]),
        Start(
            Const(lexicon["list_of_users"]),
            id="users_list",
            state=states.UsersListSG.main,
            data={"userlist_page": 1},
            on_click=close_current_dialog
        ),
        state=states.AdminMenuSG.main,
    )
)
