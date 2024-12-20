from datetime import datetime

import pytest
from aiogram import Dispatcher
from aiogram.dispatcher.event.bases import UNHANDLED
from aiogram.enums import ChatType
from aiogram.methods import SendMessage
from aiogram.methods.base import TelegramType, TelegramMethod
from aiogram.types import Update, Chat, User, Message

from bot.lexicon import lexicon
from bot.tests.mocked_aiogram import MockedBot


@pytest.mark.asyncio
async def test_cmd_start(dp: Dispatcher, bot: MockedBot) -> None:
    bot.add_result_for(
        method=SendMessage,
        ok=True
    )
    chat = Chat(id=1234567, type=ChatType.PRIVATE)
    user = User(id=1234567, is_bot=False, first_name="TestUser")
    message = Message(
        message_id=1,
        chat=chat,
        from_user=user,
        text="/start",
        date=datetime.now()
    )
    result = await dp.feed_update(
        bot,
        Update(message=message, update_id=1)
    )
    assert result is not UNHANDLED
    outgoing_message: TelegramMethod[TelegramType] = bot.get_request()
    assert isinstance(outgoing_message, SendMessage)
    assert outgoing_message.text == lexicon["/start"].format(user.first_name)
