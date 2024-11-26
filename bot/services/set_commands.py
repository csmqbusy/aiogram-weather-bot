from aiogram import Bot
from aiogram.types import BotCommand


async def set_commands(bot: Bot) -> None:
    main_menu_commands = [
        BotCommand(command="/start",
                   description="Начало работы с ботом"),
        BotCommand(command="/menu",
                   description="Главное меню со всеми доступными командами"),
    ]

    await bot.set_my_commands(main_menu_commands)
