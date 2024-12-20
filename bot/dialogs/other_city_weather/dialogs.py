from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Back, Start
from aiogram_dialog.widgets.text import Format, Const

from bot import states
from bot.api_requests.city_validator import validate_city
from bot.dialogs.common.handlers import close_current_dialog
from bot.lexicon import lexicon
from bot.dialogs.other_city_weather.getters import get_weather
from bot.dialogs.other_city_weather.handlers import (
    error_city_handler,
    correct_city_handler,
)

other_city_weather = Dialog(
    Window(
        Const(text=lexicon["enter_the_city_name"]),
        TextInput(
            id="city_selection",
            type_factory=validate_city,
            on_success=correct_city_handler,
            on_error=error_city_handler
        ),
        Start(
            Const(lexicon["cancel"]), id="main_menu",
            state=states.UserMenuSG.main,
            on_click=close_current_dialog
        ),
        state=states.OtherCityWeatherSG.city_selection,
    ),
    Window(
        Format(lexicon["weather_report"]),
        Back(Const(lexicon["choose_another_city"])),
        Start(
            Const(lexicon["to_main_menu"]),
            id="main_menu",
            state=states.UserMenuSG.main,
            on_click=close_current_dialog
        ),
        state=states.OtherCityWeatherSG.weather,
        getter=get_weather
    )
)
