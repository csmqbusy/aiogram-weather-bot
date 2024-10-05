from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def cancel_kb():
    btn1 = KeyboardButton(text="Отмена")
    markup = ReplyKeyboardMarkup(
        keyboard=[[btn1]],
        resize_keyboard=True
    )
    return markup
