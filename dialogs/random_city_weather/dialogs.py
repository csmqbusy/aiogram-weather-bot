from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.kbd import Start, Button
from aiogram_dialog.widgets.text import Format, Const

import states
from dialogs.common.handlers import close_current_dialog
from dialogs.random_city_weather.getters import get_random_city_weather
from dialogs.random_city_weather.handlers import new_random_weather_report
from lexicon import lexicon

random_city_weather = Dialog(
    Window(
        Format(lexicon["weather_report"]),
        Button(
            Const("🔄 Новый отчет"),
            id="new_random_weather_report",
            on_click=new_random_weather_report
        ),
        Start(
            Const(lexicon["to_main_menu"]),
            id="main_menu",
            state=states.UserMenuSG.main,
            on_click=close_current_dialog
        ),
        state=states.RandomCityWeatherSG.weather,
        getter=get_random_city_weather
    )
)
