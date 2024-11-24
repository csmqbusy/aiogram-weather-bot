from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.kbd import Start
from aiogram_dialog.widgets.text import Format, Const

from bot import states
from bot.lexicon import lexicon
from bot.dialogs.my_city_weather.getters import get_weather
from bot.dialogs.common.handlers import close_current_dialog

my_city_weather = Dialog(
    Window(
        Const(lexicon["no_city"], when="no_city"),
        Format(lexicon["weather_report"], when="city"),
        Start(
            Const(lexicon["change_my_city"]),
            id="change_my_city",
            state=states.SetCitySG.setup_city,
            when="city",
            on_click=close_current_dialog
        ),
        Start(
            Const(lexicon["set_my_city"]),
            id="set_my_city",
            state=states.SetCitySG.setup_city,
            when="no_city",
            on_click=close_current_dialog
        ),
        Start(
            Const(lexicon["to_main_menu"]),
            id="main_menu",
            state=states.UserMenuSG.main,
            on_click=close_current_dialog
        ),
        state=states.MyCityWeatherSG.main,
        getter=get_weather
    )
)
