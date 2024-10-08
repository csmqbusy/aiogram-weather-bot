from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Next, Button, Back, Start, Cancel
from aiogram_dialog.widgets.text import Format, Const

import states
from api_requests.city_validator import validate_city
from dialogs.set_city.getters import get_user_city
from dialogs.set_city.handlers import correct_city_setup, error_city_setup
from lexicon import lexicon

set_city = Dialog(
    Window(
        Const(lexicon["enter_the_city_name"]),
        TextInput(
            id="setup_city",
            type_factory=validate_city,
            on_success=correct_city_setup,
            on_error=error_city_setup
        ),
        Cancel(Const('Отмена'), id='button_cancel'),
        state=states.SetCitySG.setup_city,
    ),
    Window(
        Format("Запомнил, {user_city} – ваш город"),
        Start(
            Const("Узнать погоду в моем городе"),
            id="my_city_weather",
            state=states.MyCityWeatherSG.main
        ),
        Start(
            Const("В главное меню"),
            id="main_menu",
            state=states.UserMenuSG.main
        ),
        state=states.SetCitySG.city_accepted,
        getter=get_user_city
    )
)
