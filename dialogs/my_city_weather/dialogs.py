from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.kbd import Start, Group
from aiogram_dialog.widgets.text import Format, Const

import states
from lexicon import lexicon
from .getters import get_weather

my_city_weather = Dialog(
    Window(
        Const(lexicon["no_city"], when="no_city"),
        Format(lexicon["weather_report"], when="city"),
        Start(
            Const(lexicon["change_my_city"]),
            id="change_my_city",
            state=states.SetCitySG.setup_city,
            when="city"
        ),
        Start(
            Const(lexicon["set_my_city"]),
            id="set_my_city",
            state=states.SetCitySG.setup_city,
            when="no_city"
        ),
        Start(
            Const(lexicon["to_main_menu"]),
            id="main_menu",
            state=states.UserMenuSG.main
        ),
        state=states.MyCityWeatherSG.main,
        getter=get_weather
    )
)
