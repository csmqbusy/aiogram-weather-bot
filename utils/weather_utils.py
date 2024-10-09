import calendar
import json
from datetime import datetime

from database.models import WeatherReportsORM


def prepare_weather_data(w_data: dict) -> dict:
    localtime = datetime.strptime(w_data["location"]["localtime"], "%Y-%m-%d %H:%M")
    month = get_month_name_translation(localtime.strftime("%B"))
    weekday = get_weekday_name_translation(calendar.day_name[localtime.weekday()])
    date = f"{weekday} {localtime.day} {month} {localtime.year}г."
    pressure_mm = int(w_data['current']['pressure_mb']) * 0.75
    icon = w_data['current']['condition']['icon']

    weather_data = {
        "icon": icon,
        "date": date,
        "city": w_data['location']['name'],
        "country": w_data['location']['country'],
        "temp": w_data['current']['temp_c'],
        "feels_like": w_data['current']['feelslike_c'],
        "wind_speed": w_data['current']['wind_kph'],
        "pressure": str(pressure_mm),
        "visibility": w_data['current']['vis_km']
    }
    return weather_data


def prepare_report_data(report: WeatherReportsORM) -> dict:
    localtime = report.date
    month = get_month_name_translation(localtime.strftime("%B"))
    weekday = get_weekday_name_translation(calendar.day_name[localtime.weekday()])
    date = f"{weekday} {localtime.day} {month} {localtime.year}г."

    w_data = {
        "date": date,
        "city": report.city,
        "country": report.country,
        "temp": report.temp,
        "feels_like": report.feels_like,
        "wind_speed": report.wind_speed,
        "pressure": report.pressure_mm,
        "visibility": report.visibility
    }
    return w_data


def get_month_name_translation(month: str) -> str:
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


def get_weekday_name_translation(weekday: str) -> str:
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
    with open("/Users/csmq/PycharmProjects/weatherBot2/weather_example.json", 'r') as f:
        data = json.load(f)
    prepare_weather_data(data)
