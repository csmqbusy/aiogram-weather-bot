from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def user_menu_kb():
    btn1 = KeyboardButton(text="Погода в моем городе")
    btn2 = KeyboardButton(text="Погода в другом месте")
    btn3 = KeyboardButton(text="История")
    btn4 = KeyboardButton(text="Установить свой город")
    markup = ReplyKeyboardMarkup(
        keyboard=[[btn1], [btn2], [btn3], [btn4]],
        resize_keyboard=True
    )
    return markup
