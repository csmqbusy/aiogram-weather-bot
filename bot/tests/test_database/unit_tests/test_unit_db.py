from contextlib import nullcontext
from datetime import datetime
from typing import ContextManager

import pytest

from bot.database.exceptions import DatabaseError
from bot.database.models import UsersORM
from bot.database.orm import db_client


@pytest.mark.parametrize(
    "tg_id, all_checks, quantity_check",
    [
        (11111, True, False),
        (22222, False, False),
        (33333, False, True),
    ]
)
async def test_add_user(
        tg_id: int,
        all_checks: bool,
        quantity_check: bool,
) -> None:

    user = await db_client.add_user(tg_id)
    assert user.tg_id == tg_id
    if all_checks:
        assert user.city is None
        today = datetime.now().strftime("%Y-%m-%d")
        assert user.connection_date.strftime("%Y-%m-%d") == today

    if quantity_check:
        await db_client.add_user(tg_id)
        await db_client.add_user(tg_id)
        users = await db_client.get_all_users()
        assert len(users) == 1

        await db_client.add_user(tg_id * 2)
        await db_client.add_user(tg_id * 3)
        users = await db_client.get_all_users()
        assert len(users) == 3


@pytest.mark.parametrize(
    "should_add, tg_id, load_reports, return_type",
    [
        (True, 33333, False, UsersORM),
        (True, 33333, True, UsersORM),
        (False, 33333, False, None),
    ]
)
async def test__get_user(
        should_add: bool,
        tg_id: int,
        load_reports: bool,
        return_type: UsersORM | None,
) -> None:

    if should_add:
        await db_client.add_user(tg_id)

    user = await db_client._get_user(tg_id, load_reports=load_reports)
    if return_type is None:
        assert user is None
    else:
        assert isinstance(user, return_type)
        # проверяем, похоже ли на список то, что подгрузила алхимия с помощью
        # relationship, такой вариант проверки оказался самым адекватным
        if load_reports:
            assert hasattr(user.reports, "__getitem__")
            assert hasattr(user.reports, "__contains__")
            assert hasattr(user.reports, "__iter__")
            assert hasattr(user.reports, "__len__")


@pytest.mark.parametrize(
    "should_add, tg_id, city, expectation",
    [
        (True, 11111, "Сочи", nullcontext()),
        (False, 11111, "Сочи", pytest.raises(DatabaseError)),
    ]
)
async def test_set_user_city(
        should_add: True,
        tg_id: int,
        city: str,
        expectation: ContextManager,
) -> None:

    if should_add:
        await db_client.add_user(tg_id)

    with expectation:
        await db_client.set_user_city(tg_id, city)
        user_city = await db_client.get_user_city(tg_id)
        assert user_city == city


async def test_create_weather_report():
    await db_client.create_weather_report(
        tg_id=22222,
        temp=17.6,
        feels_like=16.4,
        wind_speed=4.2,
        pressure_mm=800.0,
        city="Кабардинка",
        country="Россия",
        visibility=10.0,
        weather_condition="Ясно",
    )
    user_reports = await db_client.get_user_reports(22222)
    assert len(user_reports) == 1

    report = await db_client.get_report(user_reports[0].id)
    assert report.temp == 17.6
    assert report.feels_like == 16.4
    assert report.wind_speed == 4.2
    assert report.pressure_mm == 800.0
    assert report.city == "Кабардинка"
    assert report.country == "Россия"
    assert report.visibility == 10.0
    assert report.weather_condition == "Ясно"
    today = datetime.now().strftime("%Y-%m-%d")
    assert report.date.strftime("%Y-%m-%d") == today


@pytest.mark.parametrize(
    "should_add, tg_id, expectation",
    [
        (True, 11111, nullcontext()),
        (False, 11111, pytest.raises(DatabaseError)),
    ]
)
async def test_get_user_reports(
        should_add: bool,
        tg_id: id,
        expectation: ContextManager
) -> None:

    if should_add:
        await db_client.add_user(tg_id)

    with expectation:
        reports = await db_client.get_user_reports(tg_id)
        assert hasattr(reports, "__getitem__")
        assert hasattr(reports, "__contains__")
        assert hasattr(reports, "__iter__")
        assert hasattr(reports, "__len__")

        assert len(reports) == 0


@pytest.mark.parametrize(
    "should_add, tg_id, expectation",
    [
        (True, 11111, nullcontext()),
        (False, 11111, pytest.raises(DatabaseError)),
    ]
)
async def test_delete_user_report(
        should_add: bool,
        tg_id: id,
        expectation: ContextManager
) -> None:

    if should_add:
        await db_client.add_user(tg_id)

    with expectation:
        user_reports = await db_client.get_user_reports(tg_id)
        assert len(user_reports) == 0

        for i in range(5):
            await db_client.create_weather_report(
                tg_id=tg_id,
                temp=17.6 + i,
                feels_like=16.4 + i,
                wind_speed=4.2,
                pressure_mm=800.0 + i,
                city="Кабардинка",
                country="Россия",
                visibility=10.0,
                weather_condition="Ясно",
            )

        user_reports = await db_client.get_user_reports(tg_id)
        assert len(user_reports) == 5

        await db_client.delete_user_report(user_reports[0].id)

        user_reports = await db_client.get_user_reports(tg_id)
        assert len(user_reports) == 4

        for report in user_reports:
            await db_client.delete_user_report(report.id)

        user_reports = await db_client.get_user_reports(tg_id)
        assert len(user_reports) == 0
