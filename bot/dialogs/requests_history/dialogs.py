import operator

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Row, Button, Column, Select, Back, Start
from aiogram_dialog.widgets.text import Const, Format

from bot import states
from bot.dialogs.common.handlers import close_current_dialog
from bot.dialogs.requests_history.getters import (
    get_reports_data,
    get_report_data,
)
from bot.dialogs.requests_history.handlers import (
    decrease_page, increase_page, on_report_selected, delete_request)
from bot.lexicon import lexicon

requests_history = Dialog(
    Window(
        Const(lexicon["request_history"]),
        Column(
            Select(
                Format(lexicon["report_format"]),
                id="s_reports",
                item_id_getter=operator.itemgetter(0),
                items="reports",
                on_click=on_report_selected,
            )
        ),
        Row(
            Button(Const(lexicon["back"]), id="back", on_click=decrease_page),
            Button(Format("[{page}/{n_of_pages}]"), id="current"),
            Button(Const(lexicon["forward"]), id="next", on_click=increase_page)
        ),
        Start(
            Const(lexicon["to_main_menu"]),
            id="main_menu",
            state=states.UserMenuSG.main,
            on_click=close_current_dialog
        ),
        state=states.RequestsHistorySG.main,
        getter=get_reports_data
    ),
    Window(
        Format(lexicon["show_history_report"]),
        Button(Const(lexicon["delete"]), id="delete_report",
               on_click=delete_request),
        Back(Const(lexicon["back"]), id="back"),
        Start(
            Const(lexicon["to_main_menu"]),
            id="main_menu",
            state=states.UserMenuSG.main,
            on_click=close_current_dialog
        ),
        state=states.RequestsHistorySG.report,
        getter=get_report_data
    )
)
