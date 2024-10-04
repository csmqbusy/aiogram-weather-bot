from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup

from api_requests.request import get_weather
from database.orm import db_client
from keyboards.reply.user_menu import user_menu_kb
from utils.weather_utils import prepare_weather_data, convert_weather_data_to_message
from states import SetUserCity, OtherCityWeather

router = Router()


@router.message(F.text == "Установить свой город")
async def set_user_city(message: Message, state: FSMContext):
    btn1 = KeyboardButton(text="Меню")
    markup = ReplyKeyboardMarkup(keyboard=[[btn1]])
    text = "Введите название вашего города"
    await state.set_state(SetUserCity.waiting_city)
    await message.answer(
        text=text,
        reply_markup=markup
    )


@router.message(StateFilter(SetUserCity.waiting_city))
async def user_city_chosen(message: Message, state: FSMContext):
    if message.text[0].islower():
        await message.answer("Названия городов пишутся с большой буквы")
        return
    await state.update_data(user_city=message.text)
    data = await state.get_data()
    user_city = data["user_city"]
    db_client.set_user_city(message.from_user.id, user_city)
    markup = user_menu_kb()
    text = f"Запомнил, {user_city} – ваш город"

    await message.answer(
        text=text,
        reply_markup=markup
    )
    await state.clear()


@router.message(F.text == "Погода в моем городе")
async def user_city_weather(message: Message, state: FSMContext):
    markup = user_menu_kb()

    user_city = db_client.get_user_city(message.from_user.id)
    if user_city is None:
        text = "Вы ещё не выбрали свой город.\n Можете сделать это в меню либо запросить погоду в другом месте"
        await message.answer(
            text=text,
            reply_markup=markup
        )
    else:
        weather_full_data = get_weather(user_city)
        weather_data = prepare_weather_data(weather_full_data)
        db_client.create_weather_report(
            message.from_user.id, weather_data["temp"],
            weather_data["feels_like"], weather_data["wind_speed"],
            weather_data["pressure"], weather_data["city"]
        )
        text = convert_weather_data_to_message(weather_data)

        await message.answer(
            text=text,
            reply_markup=markup
        )


@router.message(F.text == "Погода в другом месте")
async def other_city_weather(message: Message, state: FSMContext):
    btn1 = KeyboardButton(text="Меню")
    markup = ReplyKeyboardMarkup(keyboard=[[btn1]])
    text = "Введите название города"
    await state.set_state(OtherCityWeather.waiting_city)
    await message.answer(
        text=text,
        reply_markup=markup
    )


@router.message(StateFilter(OtherCityWeather.waiting_city))
async def city_chosen(message: Message, state: FSMContext):
    if message.text[0].islower():
        await message.answer("Названия городов пишутся с большой буквы")
        return
    await state.update_data(waiting_city=message.text)
    markup = user_menu_kb()

    city = message.text
    weather_full_data = get_weather(city)
    weather_data = prepare_weather_data(weather_full_data)
    db_client.create_weather_report(
        message.from_user.id, weather_data["temp"],
        weather_data["feels_like"], weather_data["wind_speed"],
        weather_data["pressure"], weather_data["city"]
    )
    text = convert_weather_data_to_message(weather_data)

    await message.answer(
        text=text,
        reply_markup=markup
    )
    await state.clear()
