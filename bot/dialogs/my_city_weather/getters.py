from typing import Any

from aiogram.types import User
from aiogram_dialog import DialogManager

from bot.api_requests.weather_request import get_weather_data
from bot.database.orm import db_client
from bot.utils.weather_reports import (
    create_weather_report,
)
from bot.utils.cache import get_weather_data_from_cache
from bot.utils.weather_utils import prepare_weather_data


async def get_weather(
        dialog_manager: DialogManager,
        event_from_user: User,
        **kwargs: dict[str, Any],
) -> dict[str, str | float]:
    user_id = event_from_user.id
    user_city = await db_client.get_user_city(user_id)
    if user_city is None:
        return {"no_city": True}

    weather_data = get_weather_data_from_cache(user_city)
    if weather_data is None:
        weather_full_data = await get_weather_data(user_city)
        weather_data = prepare_weather_data(weather_full_data)

    weather_report = create_weather_report(user_id, weather_data)
    await db_client.add_report(weather_report)
    return weather_data.model_dump()
