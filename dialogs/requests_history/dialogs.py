import operator

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Row, Button, Cancel, Column, Select, Back
from aiogram_dialog.widgets.text import Const, Format

import states
from dialogs.requests_history.getters import get_reports_data, get_report_data
from dialogs.requests_history.handlers import (decrease_page, increase_page, on_report_selected, delete_request,
                                               reset_history_page)
from lexicon import lexicon

main_menu_button = Cancel(Const("В главное меню"), id="button_cancel", on_click=reset_history_page)

requests_history = Dialog(
    Window(
        Const(lexicon["request_history"]),
        Column(
            Select(
                Format("{item[1]} {item[2]}.{item[3]}.{item[4]}"),
                id="s_reports",
                item_id_getter=operator.itemgetter(0),
                items="reports",
                on_click=on_report_selected,
            )
        ),
        Row(
            Button(Const("back"), id="back", on_click=decrease_page),
            Button(Format("{page}/{n_of_pages}"), id="current"),
            Button(Const("next"), id="next", on_click=increase_page)
        ),
        main_menu_button,
        state=states.RequestsHistorySG.main,
        getter=get_reports_data
    ),
    Window(
        Format("Данные по запросу:\n\nГород: {city}\nТемпература: {temp} °C\n"
               "Ощущается как: {feels_like} °C\nСкорость ветра: {wind_speed} км/ч\n"
               "Давление: {pressure} мм рт. ст."),
        Button(Const("Удалить запрос"), id="delete_report", on_click=delete_request),
        Back(Const("Назад"), id="back"),
        main_menu_button,
        state=states.RequestsHistorySG.report,
        getter=get_report_data
    )
)
