import pytest

from bot.database.orm import db_client
from bot.schemas import WeatherReport


@pytest.mark.parametrize(
    "tg_id, city",
    [
        (11111, "Минск")
    ]
)
async def test_set_and_get_my_city_weather(tg_id: int, city: str) -> None:
    """
    Test road:
        add_user ->
        set_user_city ->
        get_user_city ->
        create_weather_report ->
        get_user_reports ->
        delete_user_report
    """

    await db_client.add_user(tg_id)
    await db_client.set_user_city(tg_id, city)
    user_city = await db_client.get_user_city(tg_id)
    assert user_city == city
    report = WeatherReport(
        tg_id=tg_id,
        temp=0.1,
        feels_like=-1.7,
        wind_speed=5.2,
        pressure_mm=768.0,
        city=city,
        country="Беларусь",
        visibility=6.0,
        weather_condition="Пасмурно",
    )
    await db_client.add_report(report)
    user_reports = await db_client.get_user_reports(tg_id)
    assert len(user_reports) == 1

    my_city_weather_report = user_reports[0]
    assert my_city_weather_report.city == city

    await db_client.delete_user_report(my_city_weather_report.id)
    user_reports = await db_client.get_user_reports(tg_id)
    assert len(user_reports) == 0
