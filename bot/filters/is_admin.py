from aiogram.filters import BaseFilter
from aiogram.types import Message

from bot.core.config import settings


class IsAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if message.from_user is None:
            return False
        return message.from_user.id in settings.ADMINS_ID
