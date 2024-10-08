from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Next, Button, Back, Start, Cancel
from aiogram_dialog.widgets.text import Format, Const

import states
from api_requests.city_validator import validate_city
from lexicon import lexicon
from .getters import get_weather
from .handlers import error_city_handler, correct_city_handler

other_city_weather = Dialog(
    Window(
        Const(text=lexicon["enter_the_city_name"]),
        TextInput(
            id="city_selection",
            type_factory=validate_city,
            on_success=correct_city_handler,
            on_error=error_city_handler
        ),
        Cancel(Const('Отмена'), id='button_cancel'),
        state=states.OtherCityWeatherSG.city_selection,
    ),
    Window(
        Format("Погода в {city}, {counrty}:\n\n"
               "Температура: {temp} °C\n"
               "Ощущается как: {feels_like} °C\n"
               "Скорость ветра: {wind_speed} км/ч\n"
               "Давление: {pressure} мм рт. ст."),
        Back(Const("К выбору города")),
        Start(Const("В главное меню"), id="main_menu", state=states.UserMenuSG.main),
        state=states.OtherCityWeatherSG.weather,
        getter=get_weather
    )
)
