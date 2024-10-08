import requests

from settings.config import settings


def validate_city(city: str) -> None:
    r = requests.get(url='http://api.weatherapi.com/v1/current.json',
                     params={'key': settings.API_KEY,
                             'q': city})
    if r.status_code == 400:
        raise ValueError
