from datetime import datetime

import pytest

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

async def test_set_user_city():
    await db_client.set_user_city(12345, "Сочи")
    user_city = await db_client.get_user_city(12345)
    assert user_city == "Сочи"
