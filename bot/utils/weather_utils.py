import calendar
from datetime import datetime
from typing import Any

import countryflag
from translate import Translator

from bot.database.models import WeatherReportsORM
from bot.schemas import WeatherData
from bot.utils.info_from_weather_code import (
    _get_emoji_from_code,
    _get_weather_condition_from_code,
)

translator = Translator(from_lang="ru", to_lang="en")


def prepare_weather_data(w_data: dict[str, Any]) -> WeatherData:
    localtime = _parse_localtime(w_data["location"]["localtime"])
    date_string = _get_date_string(localtime)

    country = w_data["location"]["country"]
    country_emoji = _get_country_emoji(country)

    weather_data = {
        "icon": w_data["current"]["condition"]["icon"],
        "date": date_string,
        "city": w_data["location"]["name"],
        "country": country,
        "country_emoji": country_emoji,
        "temp": str(w_data["current"]["temp_c"]),
        "feels_like": str(w_data["current"]["feelslike_c"]),
        "wind_speed": str(w_data["current"]["wind_kph"]),
        "pressure": _get_pressure_mm(w_data["current"]["pressure_mb"]),
        "visibility": str(w_data["current"]["vis_km"]),
        "weather_condition": _get_weather_condition(w_data),
    }
    weather_data = WeatherData(
        icon=w_data["current"]["condition"]["icon"],
        date=date_string,
        city=w_data["location"]["name"],
        country=country,
        country_emoji=country_emoji,
        temp=w_data["current"]["temp_c"],
        feels_like=w_data["current"]["feelslike_c"],
        wind_speed=w_data["current"]["wind_kph"],
        pressure=_get_pressure_mm(w_data["current"]["pressure_mb"]),
        visibility=w_data["current"]["vis_km"],
        weather_condition=_get_weather_condition(w_data),
    )
    return weather_data


def prepare_report_data(report: WeatherReportsORM) -> dict[str, str]:
    localtime = report.date
    date_string = _get_date_string(localtime)

    w_data = {
        "date": date_string,
        "city": report.city,
        "country": report.country,
        "temp": str(report.temp),
        "feels_like": str(report.feels_like),
        "wind_speed": str(report.wind_speed),
        "pressure": str(report.pressure_mm),
        "visibility": str(report.visibility),
        "weather_condition": str(report.weather_condition),
    }
    return w_data


def _parse_localtime(
    date_string: str, pattern: str = "%Y-%m-%d %H:%M"
) -> datetime:
    return datetime.strptime(date_string, pattern)


def _get_date_string(localtime: datetime) -> str:
    month_ru = _get_month_name_translation(localtime.strftime("%B"))
    weekday_name_en = _get_weekday_name(localtime)
    weekday_name_ru = _get_weekday_name_translation(weekday_name_en)
    return f"{weekday_name_ru} {localtime.day} {month_ru} {localtime.year}г."


def _get_weekday_name(localtime: datetime) -> str:
    return calendar.day_name[localtime.weekday()]


def _get_pressure_mm(pressure_mb: float) -> float:
    return round(pressure_mb * 0.75, 2)


def _get_weather_condition(w_data: dict[str, Any]) -> str:
    code = w_data["current"]["condition"]["code"]
    is_day = bool(w_data["current"]["is_day"])
    emoji = _get_emoji_from_code(code)
    weather_condition = _get_weather_condition_from_code(code, is_day)
    return f"{emoji} {weather_condition}"


def _get_country_emoji(country: str) -> str:
    if _is_russian_country_name(country):
        country = _translate_country_name(country)
    try:
        country_emoji = str(countryflag.getflag([country]))
    except Exception:  # noqa
        country_emoji = "🏳"
    return country_emoji


def _is_russian_country_name(country: str) -> bool:
    russian_letters = [
        'а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л', 'м',
        'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ',
        'ы', 'ь', 'э', 'ю', 'я'
    ]
    country = country.lower()
    return country[0] in russian_letters or country[1] in russian_letters


def _translate_country_name(country: str) -> str:
    country_en = str(translator.translate(country))
    return country_en


def _get_month_name_translation(month: str) -> str:
    months = {
        "january": "января",
        "february": "февраля",
        "march": "марта",
        "april": "апреля",
        "may": "мая",
        "june": "июня",
        "july": "июля",
        "august": "августа",
        "september": "сентября",
        "october": "октября",
        "november": "ноября",
        "december": "декабря",
    }
    return months[month.lower()]


def _get_weekday_name_translation(weekday: str) -> str:
    days = {
        "monday": "понедельник",
        "tuesday": "вторник",
        "wednesday": "среда",
        "thursday": "четверг",
        "friday": "пятница",
        "saturday": "суббота",
        "sunday": "воскресенье",
    }
    return days.get(weekday.lower(), "неизвестно")
