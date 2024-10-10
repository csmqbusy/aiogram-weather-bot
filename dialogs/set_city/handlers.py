from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import ManagedTextInput

from database.orm import db_client
from lexicon import lexicon


async def error_city_setup(message: Message,
                           widget: ManagedTextInput,
                           dialog_manager: DialogManager,
                           error: ValueError):
    await message.answer(
        text=lexicon["incorrect_city_name"]
    )


async def correct_city_setup(message: Message,
                             widget: ManagedTextInput,
                             dialog_manager: DialogManager,
                             text: str):
    user_city = message.text
    await db_client.set_user_city(message.from_user.id, user_city)
    dialog_manager.dialog_data.update(user_city=user_city)
    await dialog_manager.next()
