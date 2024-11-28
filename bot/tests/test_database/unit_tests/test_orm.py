from datetime import datetime

import pytest

from bot.database.orm import db_client


async def test_add_user():
    user = await db_client.add_user(12345)
    assert user.tg_id == 12345
    assert user.city is None
    today = datetime.now().strftime("%Y-%m-%d")
    assert user.connection_date.strftime("%Y-%m-%d") == today


async def test_set_user_city():
    await db_client.set_user_city(12345, "Сочи")
    user_city = await db_client.get_user_city(12345)
    assert user_city == "Сочи"
