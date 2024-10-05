import json

import requests

from settings.config import settings


def get_weather_data(city: str):
    r = requests.get(url='http://api.weatherapi.com/v1/current.json',
                     params={
                         'key': settings.API_KEY,
                         'q': city
                     })
    return json.loads(r.text)
