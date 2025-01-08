import logging

from bot.schemas import WeatherReport, WeatherData

logger = logging.getLogger(__name__)


def create_weather_report(
        user_id: int,
        weather_data: WeatherData
) -> WeatherReport:
    return WeatherReport(
        tg_id=user_id,
        temp=weather_data.temp,
        feels_like=weather_data.feels_like,
        wind_speed=weather_data.wind_speed,
        pressure_mm=weather_data.pressure,
        city=weather_data.city,
        country=weather_data.country,
        visibility=weather_data.visibility,
        weather_condition=weather_data.weather_condition,
    )
