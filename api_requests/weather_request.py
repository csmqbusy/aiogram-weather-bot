import logging

import aiohttp
from requests import ReadTimeout

from settings.config import settings


async def get_weather_data(city: str) -> dict:
    while True:
        try:
            weather_data = await _get_data(city)
        except Exception as e:
            logging.info(f"Request to http://api.weatherapi.com: {e}")
            continue
        return weather_data


async def _get_data(city: str) -> dict:
    async with aiohttp.ClientSession(read_timeout=3) as session:
        url = 'http://api.weatherapi.com/v1/current.json'
        params = {'key': settings.API_KEY, 'q': city}
        async with session.get(url=url, params=params) as response:
            return await response.json()
