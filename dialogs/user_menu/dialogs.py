from aiogram_dialog import Dialog, Window, StartMode
from aiogram_dialog.widgets.kbd import Start
from aiogram_dialog.widgets.text import Const

import states
from lexicon import lexicon

user_menu = Dialog(
    Window(
        Const(lexicon["main_menu_user"]),
        Start(
            Const(lexicon["user_city_weather"]),
            id="my_city_weather",
            state=states.MyCityWeatherSG.main
        ),
        Start(
            Const(lexicon["other_city_weather"]),
            id="other_city_weather",
            state=states.OtherCityWeatherSG.city_selection,
        ),
        Start(
            Const(lexicon["history"]),
            id="requests_history",
            state=states.RequestsHistorySG.main,
            data={"history_page": 1}
        ),
        Start(
            Const(lexicon["set_my_city"]),
            id="set_city",
            state=states.SetCitySG.setup_city,
        ),
        state=states.UserMenuSG.main,
    )
)
