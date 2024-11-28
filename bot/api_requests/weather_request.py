import asyncio
import logging
from typing import Any

import aiohttp

from bot.api_requests.exceptions import RequestError
from bot.settings.config import settings


logger = logging.getLogger(__name__)


async def get_weather_data(city: str) -> dict[str, Any]:
    attempts = 10
    current_attempts = 0
    while current_attempts < attempts:
        try:
            weather_data = await _get_data(city)
        except Exception as e:
            logger.warning(f"Request to http://api.weatherapi.com: {e}")
            current_attempts += 1
            sleep_ = 0.25
            logger.info(f"Next attempt to send a request in {sleep_}s")
            await asyncio.sleep(sleep_)
            continue
        return weather_data
    raise RequestError("Can't get weather data")


async def _get_data(city: str) -> dict[str, Any]:
    async with aiohttp.ClientSession(read_timeout=3) as session:
        url = "http://api.weatherapi.com/v1/current.json"
        params = {"key": settings.API_KEY, "q": city}
        async with session.get(url=url, params=params) as response:
            data = await response.json()
            return dict(data)
