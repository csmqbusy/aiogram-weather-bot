import requests

from settings.config import settings


def validate_city(city: str) -> bool:
    r = requests.get(url='http://api.weatherapi.com/v1/current.json',
                     params={'key': settings.API_KEY,
                             'q': city})
    return r.status_code != 400
