from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from lexicon import lexicon


def cancel_kb():
    btn1 = KeyboardButton(text=lexicon["cancel"])
    markup = ReplyKeyboardMarkup(
        keyboard=[[btn1]],
        resize_keyboard=True
    )
    return markup
