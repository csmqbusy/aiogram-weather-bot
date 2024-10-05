from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from lexicon import lexicon


def user_menu_kb():
    btn1 = KeyboardButton(text=lexicon["user_city_weather"])
    btn2 = KeyboardButton(text=lexicon["other_city_weather"])
    btn3 = KeyboardButton(text=lexicon["history"])
    btn4 = KeyboardButton(text=lexicon["set_your_city"])
    markup = ReplyKeyboardMarkup(
        keyboard=[[btn1], [btn2], [btn3], [btn4]],
        resize_keyboard=True
    )
    return markup
