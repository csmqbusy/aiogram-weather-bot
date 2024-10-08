from .admin_menu import admin_menu
from .list_of_users import user_list
from .user_menu import user_menu
from .my_city_weather import my_city_weather
from .other_city_weather import other_city_weather
from .set_city import set_city
from .requests_history import requests_history

all_dialogs = [
    admin_menu,
    user_list,
    user_menu,
    my_city_weather,
    other_city_weather,
    set_city,
    requests_history
]
