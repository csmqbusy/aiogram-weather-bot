from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Start
from aiogram_dialog.widgets.text import Const

import states
from lexicon import lexicon

user_menu = Dialog(
    Window(
        Const(lexicon["main_menu_user"]),
        Start(
            Const("Погода в моем городе"),
            id="my_city_weather",
            state=states.MyCityWeatherSG.main
        ),
        Start(
            Const("Погода в другом месте"),
            id="other_city_weather",
            state=states.OtherCityWeatherSG.city_selection,
        ),
        Start(
            Const("История"),
            id="requests_history",
            state=states.RequestsHistorySG.main,
        ),
        Start(
            Const("Установить свой город"),
            id="set_city",
            state=states.SetCitySG.setup_city,
        ),
        state=states.UserMenuSG.main,
    )
)
