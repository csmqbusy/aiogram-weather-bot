from contextlib import nullcontext
from datetime import datetime

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
        # relationship, такой вариант проверки оказался самым действенным
        if load_reports:
            assert hasattr(user.reports, "__getitem__")
            assert hasattr(user.reports, "__contains__")
            assert hasattr(user.reports, "__iter__")
            assert hasattr(user.reports, "__len__")
