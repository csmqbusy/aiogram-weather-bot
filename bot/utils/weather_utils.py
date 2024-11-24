import calendar
import json
from datetime import datetime

import countryflag
from translate import Translator

from bot.database.models import WeatherReportsORM
from bot.utils.info_from_weather_code import (
    get_emoji_from_code,
    get_weather_condition_from_code,
)

translator = Translator(from_lang="ru", to_lang="en")


def prepare_weather_data(w_data: dict) -> dict:
    localtime = datetime.strptime(
        w_data["location"]["localtime"], "%Y-%m-%d %H:%M"
    )
    month = _get_month_name_translation(localtime.strftime("%B"))
    weekday = _get_weekday_name_translation(
        calendar.day_name[localtime.weekday()]
    )
    date = f"{weekday} {localtime.day} {month} {localtime.year}г."
    pressure_mm = round(float(w_data['current']['pressure_mb']) * 0.75, 2)
    icon = w_data['current']['condition']['icon']
    code = w_data['current']['condition']['code']
    is_day = bool(w_data['current']['is_day'])
    emoji = get_emoji_from_code(code)
    weather_condition = get_weather_condition_from_code(code, is_day)
    country = w_data['location']['country']
    country_emoji = get_country_emoji(country)

    weather_data = {
        "icon": icon,
        "date": date,
        "city": w_data['location']['name'],
        "country": country,
        "country_emoji": country_emoji,
        "temp": w_data['current']['temp_c'],
        "feels_like": w_data['current']['feelslike_c'],
        "wind_speed": w_data['current']['wind_kph'],
        "pressure": pressure_mm,
        "visibility": w_data['current']['vis_km'],
        "weather_condition": f"{emoji} {weather_condition}",
    }
    return weather_data


def prepare_report_data(report: WeatherReportsORM) -> dict:
    localtime = report.date
    month = _get_month_name_translation(localtime.strftime("%B"))
    weekday = _get_weekday_name_translation(
        calendar.day_name[localtime.weekday()]
    )
    date = f"{weekday} {localtime.day} {month} {localtime.year}г."

    w_data = {
        "date": date,
        "city": report.city,
        "country": report.country,
        "temp": report.temp,
        "feels_like": report.feels_like,
        "wind_speed": report.wind_speed,
        "pressure": report.pressure_mm,
        "visibility": report.visibility,
        "weather_condition": report.weather_condition
    }
    return w_data


def get_country_emoji(country: str) -> str:
    if _is_russian_country_name(country):
        country = _translate_country_name(country)
    try:
        country_emoji = countryflag.getflag([country])
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
    country_en = translator.translate(country)
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
        "december": "декабря"
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
        "sunday": "воскресенье"
    }
    return days[weekday.lower()]


if __name__ == '__main__':
    filepath = "/weather_example.json"
    with open(filepath, 'r') as f:
        data = json.load(f)
    prepare_weather_data(data)
