from aiogram.types import User
from aiogram_dialog import DialogManager

from api_requests.request import get_weather_data
from database.orm import db_client
from utils.weather_utils import prepare_weather_data


async def get_weather(dialog_manager: DialogManager, event_from_user: User, **kwargs):
    user_id = event_from_user.id
    user_city = db_client.get_user_city(user_id)
    weather_full_data = get_weather_data(user_city)
    weather_data = prepare_weather_data(weather_full_data)
    db_client.create_weather_report(
        user_id, weather_data["temp"],
        weather_data["feels_like"], weather_data["wind_speed"],
        weather_data["pressure"], weather_data["city"]
    )
    return weather_data
