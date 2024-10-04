from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def admin_menu_kb():
    btn1 = KeyboardButton(text="Список пользователей")
    markup = ReplyKeyboardMarkup(
        keyboard=[[btn1]]
    )
    return markup
