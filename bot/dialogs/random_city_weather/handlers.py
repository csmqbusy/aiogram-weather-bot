from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager

from bot import states


async def new_random_weather_report(
        callback: CallbackQuery,
        widget: Any,
        dialog_manager: DialogManager
) -> None:
    await dialog_manager.switch_to(states.RandomCityWeatherSG.weather)
