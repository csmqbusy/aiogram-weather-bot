import aiohttp

from settings.config import settings


async def get_weather_data(city: str):
    async with aiohttp.ClientSession() as session:
        url = 'http://api.weatherapi.com/v1/current.json'
        params = {'key': settings.API_KEY, 'q': city}
        async with session.get(url=url, params=params) as response:
            return await response.json()
