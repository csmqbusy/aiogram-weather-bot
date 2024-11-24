from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Start
from aiogram_dialog.widgets.text import Format, Const

from bot import states
from bot.api_requests.city_validator import validate_city
from bot.dialogs.common.handlers import close_current_dialog
from bot.dialogs.set_city.getters import get_user_city
from bot.dialogs.set_city.handlers import correct_city_setup, error_city_setup
from bot.lexicon import lexicon

set_city = Dialog(
    Window(
        Const(lexicon["enter_the_city_name"]),
        TextInput(
            id="setup_city",
            type_factory=validate_city,
            on_success=correct_city_setup,
            on_error=error_city_setup
        ),
        Start(
            Const(lexicon["cancel"]),
            id="main_menu",
            state=states.UserMenuSG.main,
            on_click=close_current_dialog
        ),
        state=states.SetCitySG.setup_city,
    ),
    Window(
        Format(lexicon["set_my_city_fbk"]),
        Start(
            Const(lexicon["get_the_weather_in_my_city"]),
            id="my_city_weather",
            state=states.MyCityWeatherSG.main,
            on_click=close_current_dialog
        ),
        Start(
            Const(lexicon["to_main_menu"]),
            id="main_menu",
            state=states.UserMenuSG.main,
            on_click=close_current_dialog
        ),
        state=states.SetCitySG.city_accepted,
        getter=get_user_city
    )
)
