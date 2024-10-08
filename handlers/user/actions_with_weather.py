from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from api_requests.city_validator import validate_city
from api_requests.request import get_weather_data
from database.orm import db_client
from handlers.user.commands import menu_cmd
from keyboards.reply.other_keyboards import cancel_kb
from keyboards.reply.user_menu import user_menu_kb
from lexicon import lexicon
from utils.weather_utils import prepare_weather_data, convert_weather_data_to_message
from states_old import SetUserCity, OtherCityWeather

router = Router()


@router.message(F.text == lexicon["set_your_city"])
async def set_user_city(message: Message, state: FSMContext):
    markup = cancel_kb()
    await state.set_state(SetUserCity.waiting_city)
    await message.answer(
        text=lexicon["enter_the_city_name"],
        reply_markup=markup
    )


@router.message(StateFilter(SetUserCity.waiting_city), F.text == lexicon["cancel"])
@router.message(StateFilter(OtherCityWeather.waiting_city), F.text == lexicon["cancel"])
async def user_city_cancel(message: Message, state: FSMContext):
    await menu_cmd(message)
    await state.clear()


@router.message(StateFilter(SetUserCity.waiting_city))
async def user_city_chosen(message: Message, state: FSMContext):
    if validate_city(message.text):
        await state.update_data(user_city=message.text)
        data = await state.get_data()
        user_city = data["user_city"]
        db_client.set_user_city(message.from_user.id, user_city)
        markup = user_menu_kb()
        await message.answer(
            text=lexicon["set_your_city_fbk"].format(user_city),
            reply_markup=markup
        )
        await state.clear()
    else:
        markup = cancel_kb()
        await message.answer(
            text=lexicon["incorrect_city_name"],
            reply_markup=markup
        )


@router.message(F.text == lexicon["user_city_weather"])
async def user_city_weather(message: Message):
    markup = user_menu_kb()
    user_city = db_client.get_user_city(message.from_user.id)
    if user_city is None:
        await message.answer(
            text=lexicon["no_user_city"],
            reply_markup=markup
        )
    else:
        weather_full_data = get_weather_data(user_city)
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


@router.message(F.text == lexicon["other_city_weather"])
async def other_city_weather(message: Message, state: FSMContext):
    markup = cancel_kb()
    await state.set_state(OtherCityWeather.waiting_city)
    await message.answer(
        text=lexicon["enter_the_city_name"],
        reply_markup=markup
    )


@router.message(StateFilter(OtherCityWeather.waiting_city))
async def city_chosen(message: Message, state: FSMContext):
    if validate_city(message.text):
        await state.update_data(waiting_city=message.text)
        markup = user_menu_kb()
        city = message.text
        weather_full_data = get_weather_data(city)
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
    else:
        markup = cancel_kb()
        await message.answer(
            text=lexicon["incorrect_city_name"],
            reply_markup=markup
        )
