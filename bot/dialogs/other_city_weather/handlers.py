from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import ManagedTextInput

from bot.lexicon import lexicon


async def error_city_handler(
        message: Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        error: ValueError
) -> None:
    await message.answer(text=lexicon["incorrect_city_name"])


async def correct_city_handler(
        message: Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        text: str
) -> None:
    dialog_manager.dialog_data.update(city=message.text)
    await dialog_manager.next()
