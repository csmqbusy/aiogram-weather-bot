from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Start
from aiogram_dialog.widgets.text import Const

import states
from dialogs.common.handlers import close_current_dialog
from lexicon import lexicon

user_menu = Dialog(
    Window(
        Const(lexicon["main_menu_user"]),
        Start(
            Const(lexicon["user_city_weather"]),
            id="my_city_weather",
            state=states.MyCityWeatherSG.main,
            on_click=close_current_dialog
        ),
        Start(
            Const(lexicon["other_city_weather"]),
            id="other_city_weather",
            state=states.OtherCityWeatherSG.city_selection,
            on_click=close_current_dialog
        ),
        Start(
            Const(lexicon["random_city_weather"]),
            id="random_city_weather",
            state=states.RandomCityWeatherSG.weather,
            on_click=close_current_dialog
        ),
        Start(
            Const(lexicon["history"]),
            id="requests_history",
            state=states.RequestsHistorySG.main,
            data={"history_page": 1},
            on_click=close_current_dialog
        ),
        Start(
            Const(lexicon["set_my_city"]),
            id="set_city",
            state=states.SetCitySG.setup_city,
            on_click=close_current_dialog
        ),
        state=states.UserMenuSG.main,
    )
)
