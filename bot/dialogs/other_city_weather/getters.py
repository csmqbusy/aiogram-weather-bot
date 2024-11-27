from aiogram.types import User
from aiogram_dialog import DialogManager

from bot.api_requests.weather_request import get_weather_data
from bot.database.orm import db_client
from bot.utils.weather_utils import prepare_weather_data


async def get_weather(
        dialog_manager: DialogManager,
        event_from_user: User,
        **kwargs,
) -> dict[str, str]:
    city = dialog_manager.dialog_data["city"]
    user_id = event_from_user.id
    weather_full_data = await get_weather_data(city)
    weather_data = prepare_weather_data(weather_full_data)
    await db_client.create_weather_report(
        user_id,
        float(weather_data["temp"]),
        float(weather_data["feels_like"]),
        float(weather_data["wind_speed"]),
        float(weather_data["pressure"]),
        weather_data["city"],
        weather_data["country"],
        float(weather_data["visibility"]),
        weather_data["weather_condition"],
    )
    return weather_data
