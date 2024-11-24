import rcoc
from aiogram.types import User
from aiogram_dialog import DialogManager

from bot.api_requests.weather_request import get_weather_data
from bot.database.orm import db_client
from bot.utils.weather_utils import prepare_weather_data


async def get_random_city_weather(dialog_manager: DialogManager,
                                  event_from_user: User, **kwargs):
    weather_full_data = {"error": "blank"}
    while "error" in weather_full_data:
        random_city = rcoc.get_random_city()
        weather_full_data = await get_weather_data(random_city)

    user_id = event_from_user.id
    weather_data = prepare_weather_data(weather_full_data)
    await db_client.create_weather_report(
        user_id, weather_data["temp"],
        weather_data["feels_like"], weather_data["wind_speed"],
        weather_data["pressure"], weather_data["city"],
        weather_data["country"], weather_data["visibility"],
        weather_data["weather_condition"]
    )
    return weather_data
