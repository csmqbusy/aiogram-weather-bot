import aiohttp
import requests

from bot.settings.config import settings


async def validate_city_aio(city: str) -> None:
    async with aiohttp.ClientSession() as session:
        url = 'http://api.weatherapi.com/v1/current.json'
        params = {'key': settings.API_KEY, 'q': city}
        async with session.get(url=url, params=params) as response:
            if response.status == 400:
                raise ValueError


def validate_city(city: str) -> str:
    r = requests.get(
        url='http://api.weatherapi.com/v1/current.json',
        params={
            'key': settings.API_KEY,
            'q': city
        }
    )
    if r.status_code != 400:
        return str(r.status_code)
    raise ValueError
