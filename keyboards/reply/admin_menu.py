from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from lexicon import lexicon


def admin_menu_kb():
    btn1 = KeyboardButton(text=lexicon["list_of_users"])
    markup = ReplyKeyboardMarkup(
        keyboard=[[btn1]],
        resize_keyboard=True
    )
    return markup
