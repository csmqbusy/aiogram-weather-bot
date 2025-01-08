from pydantic import BaseModel


class WeatherData(BaseModel):
    icon: str
    date: str
    city: str
    country: str
    country_emoji: str
    temp: float
    feels_like: float
    wind_speed: float
    pressure: float
    visibility: float
    weather_condition: str
