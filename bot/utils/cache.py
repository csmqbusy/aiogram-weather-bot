import json
from datetime import timedelta

from bot.cache.redis_config import redis_client
from bot.schemas import WeatherData
from bot.utils.weather_reports import logger


def add_weather_data_to_cache(
        weather_report: WeatherData,
        seconds: int | timedelta = 60
) -> None:
    cache_key = f"weather_data:{weather_report.city}"
    redis_client.setex(
        name=cache_key,
        time=seconds,
        value=json.dumps(weather_report.model_dump())
    )


def get_weather_data_from_cache(city: str) -> WeatherData | None:
    cache_key = f"weather_data:{city}"
    if cached_data := redis_client.get(cache_key):
        logger.info(f"Returning cached data for {city} weather")
        return WeatherData.model_validate_json(str(cached_data))
    return None
