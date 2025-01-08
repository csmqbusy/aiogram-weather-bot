from pydantic import BaseModel


class WeatherReport(BaseModel):
    tg_id: int
    temp: float
    feels_like: float
    wind_speed: float
    pressure_mm: float
    city: str
    country: str
    visibility: float
    weather_condition: str
