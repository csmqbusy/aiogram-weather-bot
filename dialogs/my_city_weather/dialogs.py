from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.kbd import Start
from aiogram_dialog.widgets.text import Format, Const

import states
from .getters import get_weather

my_city_weather = Dialog(
    Window(
        Format("Погода в {city}, {counrty}:\n\n"
               "Температура: {temp} °C\n"
               "Ощущается как: {feels_like} °C\n"
               "Скорость ветра: {wind_speed} км/ч\n"
               "Давление: {pressure} мм рт. ст."),
        Start(
            Const("Изменить мой город"),
            id="change_my_city",
            state=states.SetCitySG.setup_city
        ),
        Start(
            Const("В главное меню"),
            id="main_menu",
            state=states.UserMenuSG.main
        ),
        state=states.MyCityWeatherSG.main,
        getter=get_weather
    )
)
