from logging import basicConfig, INFO
import math

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, StateFilter, BaseFilter
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

from settings.config import settings
from api_requests.request import get_weather
from utils.weather_utils import prepare_weather_data, convert_weather_data_to_message
from database.orm import db_client

bot = Bot(token=settings.BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


class ChoiseCityWeather(StatesGroup):
    waiting_city = State()


class SetUserCity(StatesGroup):
    waiting_city = State()


class ReportsActionsCb(CallbackData, prefix='reports_actions'):
    action: str
    value: int


class AdminsActionsCb(CallbackData, prefix='admins_actions'):
    action: str
    value: int


class IsAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in settings.ADMINS_ID


@dp.message(F.text == "Меню")
@dp.message(Command(commands=['start']))
async def start_cmd(message: Message):
    db_client.add_user(message.from_user.id)
    btn1 = KeyboardButton(text="Погода в моем городе")
    btn2 = KeyboardButton(text="Погода в другом месте")
    btn3 = KeyboardButton(text="История")
    btn4 = KeyboardButton(text="Установить свой город")
    markup = ReplyKeyboardMarkup(keyboard=[[btn1], [btn2], [btn3], [btn4]])
    text = f"Привет, {message.from_user.first_name}! Я бот, который расскажет тебе о погоде на сегодня"
    await message.answer(
        text=text,
        reply_markup=markup
    )


@dp.message(F.text == "Установить свой город")
async def set_user_city(message: Message, state: FSMContext):
    btn1 = KeyboardButton(text="Меню")
    markup = ReplyKeyboardMarkup(keyboard=[[btn1]])
    text = "Введите название вашего города"
    await state.set_state(SetUserCity.waiting_city)
    await message.answer(
        text=text,
        reply_markup=markup
    )


@dp.message(StateFilter(SetUserCity.waiting_city))
async def user_city_chosen(message: Message, state: FSMContext):
    if message.text[0].islower():
        await message.answer("Названия городов пишутся с большой буквы")
        return
    await state.update_data(user_city=message.text)
    data = await state.get_data()
    user_city = data["user_city"]
    db_client.set_user_city(message.from_user.id, user_city)
    btn1 = KeyboardButton(text="Погода в моем городе")
    btn2 = KeyboardButton(text="Погода в другом месте")
    btn3 = KeyboardButton(text="История")
    btn4 = KeyboardButton(text="Установить свой город")
    markup = ReplyKeyboardMarkup(keyboard=[[btn1], [btn2], [btn3], [btn4]])
    text = f"Запомнил, {user_city} – ваш город"

    await message.answer(
        text=text,
        reply_markup=markup
    )
    await state.clear()


@dp.message(F.text == "Погода в моем городе")
async def user_city_weather(message: Message, state: FSMContext):
    btn1 = KeyboardButton(text="Погода в моем городе")
    btn2 = KeyboardButton(text="Погода в другом месте")
    btn3 = KeyboardButton(text="История")
    btn4 = KeyboardButton(text="Установить свой город")
    markup = ReplyKeyboardMarkup(keyboard=[[btn1], [btn2], [btn3], [btn4]])

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


@dp.message(F.text == "Погода в другом месте")
async def other_city_weather(message: Message, state: FSMContext):
    btn1 = KeyboardButton(text="Меню")
    markup = ReplyKeyboardMarkup(keyboard=[[btn1]])
    text = "Введите название города"
    await state.set_state(ChoiseCityWeather.waiting_city)
    await message.answer(
        text=text,
        reply_markup=markup
    )


@dp.message(StateFilter(ChoiseCityWeather.waiting_city))
async def city_chosen(message: Message, state: FSMContext):
    if message.text[0].islower():
        await message.answer("Названия городов пишутся с большой буквы")
        return
    await state.update_data(waiting_city=message.text)
    btn1 = KeyboardButton(text="Погода в моем городе")
    btn2 = KeyboardButton(text="Погода в другом месте")
    btn3 = KeyboardButton(text="История")
    btn4 = KeyboardButton(text="Установить свой город")
    markup = ReplyKeyboardMarkup(keyboard=[[btn1], [btn2], [btn3], [btn4]])

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


@dp.message(F.text == "История")
async def get_reports(message: Message):
    current_page = 1
    reports = db_client.get_user_reports(message.from_user.id)
    total_pages = math.ceil(len(reports) / 4)
    text = "История запросов:"
    buttons = []
    for report in reports[:current_page * 4]:
        buttons.append(
            [
                InlineKeyboardButton(
                    text=f"{report.city} {report.date.day}.{report.date.month}.{report.date.year}",
                    callback_data=ReportsActionsCb(action="report", value=report.id).pack()
                )
            ]
        )
    current_page += 1
    button_page = InlineKeyboardButton(
        text=f"{current_page - 1}/{total_pages}",
        callback_data=ReportsActionsCb(action="None", value=0).pack()
    )
    button_next = InlineKeyboardButton(
        text=f"Вперед",
        callback_data=ReportsActionsCb(action="next", value=current_page).pack()
    )
    markup = InlineKeyboardMarkup(
        inline_keyboard=[*buttons, [button_page, button_next]]
    )

    await message.answer(
        text=text,
        reply_markup=markup
    )


@dp.callback_query(ReportsActionsCb.filter(F.action == "next"))
async def callback_next_reports_page(query: CallbackQuery, callback_data: CallbackData,
                                     state: FSMContext):
    await state.update_data(current_page=callback_data.value)
    current_page = callback_data.value
    reports = db_client.get_user_reports(query.from_user.id)
    total_pages = math.ceil(len(reports) / 4)
    if current_page * 4 >= len(reports):
        buttons = []
        for report in reports[current_page * 4 - 4: len(reports) + 1]:
            buttons.append(
                [
                    InlineKeyboardButton(
                        text=f"{report.city} {report.date.day}.{report.date.month}.{report.date.year}",
                        callback_data=ReportsActionsCb(action="report", value=report.id).pack()
                    )
                ]
            )
        current_page -= 1
        await state.update_data(current_page=current_page)
        button_page = InlineKeyboardButton(
            text=f"{current_page + 1}/{total_pages}",
            callback_data=ReportsActionsCb(action="page_status", value=current_page).pack()
        )
        button_prev = InlineKeyboardButton(
            text=f"Назад",
            callback_data=ReportsActionsCb(action="prev", value=current_page).pack()
        )
        markup = InlineKeyboardMarkup(
            inline_keyboard=[*buttons, [button_prev, button_page]]
        )
        await query.message.edit_text(
            text="История запросов:",
            reply_markup=markup
        )
    else:
        buttons = []
        for report in reports[current_page * 4 - 4: current_page * 4]:
            buttons.append(
                [
                    InlineKeyboardButton(
                        text=f"{report.city} {report.date.day}.{report.date.month}.{report.date.year}",
                        callback_data=ReportsActionsCb(action="report", value=report.id).pack()
                    )
                ]
            )
        current_page += 1
        await state.update_data(current_page=current_page)
        button_page = InlineKeyboardButton(
            text=f"{current_page - 1}/{total_pages}",
            callback_data=ReportsActionsCb(action="page_status", value=current_page).pack()
        )
        button_prev = InlineKeyboardButton(
            text=f"Назад",
            callback_data=ReportsActionsCb(action="prev", value=current_page - 2).pack()
        )
        button_next = InlineKeyboardButton(
            text=f"Вперед",
            callback_data=ReportsActionsCb(action="next", value=current_page).pack()
        )
        markup = InlineKeyboardMarkup(
            inline_keyboard=[*buttons, [button_prev, button_page, button_next]]
        )
        await query.message.edit_text(
            text="История запросов:",
            reply_markup=markup
        )


@dp.callback_query(ReportsActionsCb.filter(F.action == "prev"))
async def callback_prev_reports_page(query: CallbackQuery, callback_data: CallbackData,
                                     state: FSMContext):
    await state.update_data(current_page=callback_data.value)
    current_page = callback_data.value
    reports = db_client.get_user_reports(query.from_user.id)
    total_pages = math.ceil(len(reports) / 4)
    if current_page == 1:
        buttons = []
        for report in reports[:current_page * 4]:
            buttons.append(
                [
                    InlineKeyboardButton(
                        text=f"{report.city} {report.date.day}.{report.date.month}.{report.date.year}",
                        callback_data=ReportsActionsCb(action="report", value=report.id).pack()
                    )
                ]
            )
        current_page += 1
        await state.update_data(current_page=current_page)
        button_page = InlineKeyboardButton(
            text=f"{current_page - 1}/{total_pages}",
            callback_data=ReportsActionsCb(action="page_status", value=current_page).pack()
        )
        button_next = InlineKeyboardButton(
            text=f"Вперед",
            callback_data=ReportsActionsCb(action="next", value=current_page).pack()
        )
        markup = InlineKeyboardMarkup(
            inline_keyboard=[*buttons, [button_page, button_next]]
        )
        await query.message.edit_text(
            text="История запросов:",
            reply_markup=markup
        )
    else:
        buttons = []
        for report in reports[current_page * 4 - 4: current_page * 4]:
            buttons.append(
                [
                    InlineKeyboardButton(
                        text=f"{report.city} {report.date.day}.{report.date.month}.{report.date.year}",
                        callback_data=ReportsActionsCb(action="report", value=report.id).pack()
                    )
                ]
            )
        current_page -= 1
        await state.update_data(current_page=current_page)
        button_page = InlineKeyboardButton(
            text=f"{current_page + 1}/{total_pages}",
            callback_data=ReportsActionsCb(action="page_status", value=current_page).pack()
        )
        button_prev = InlineKeyboardButton(
            text=f"Назад",
            callback_data=ReportsActionsCb(action="prev", value=current_page).pack()
        )
        button_next = InlineKeyboardButton(
            text=f"Вперед",
            callback_data=ReportsActionsCb(action="next", value=current_page).pack()
        )
        markup = InlineKeyboardMarkup(
            inline_keyboard=[*buttons, [button_prev, button_page, button_next]]
        )
        await query.message.edit_text(
            text="История запросов:",
            reply_markup=markup
        )


@dp.callback_query(ReportsActionsCb.filter(F.action == "report"))
async def callback_show_report(query: CallbackQuery, callback_data: CallbackData,
                               state: FSMContext):
    report_id = callback_data.value
    reports = db_client.get_user_reports(query.from_user.id)
    for report in reports:
        if report.id == int(report_id):
            button_back = InlineKeyboardButton(
                text="Назад",
                callback_data="back_to_history"
            )
            button_delete = InlineKeyboardButton(
                text="Удалить запрос",
                callback_data=ReportsActionsCb(action="delete", value=report_id).pack()
            )
            markup = InlineKeyboardMarkup(
                inline_keyboard=[[button_back], [button_delete]]
            )
            text = ("Данные по запросу:\n\n"
                    f"Город: {report.city}\n"
                    f"Температура: {report.temp} °C\n"
                    f"Ощущается как: {report.feels_like} °C\n"
                    f"Скорость ветра: {report.wind_speed} км/ч\n"
                    f"Давление: {report.pressure_mm} мм рт. ст.")
            await query.message.edit_text(
                text=text,
                reply_markup=markup
            )


@dp.callback_query(F.data == "back_to_history")
async def back_to_history(query: CallbackQuery, state: FSMContext):
    current_page = 1
    await state.update_data(current_page=current_page)
    reports = db_client.get_user_reports(query.from_user.id)
    total_pages = math.ceil(len(reports) / 4)
    text = "История запросов:"
    buttons = []
    for report in reports[:current_page * 4]:
        buttons.append(
            [
                InlineKeyboardButton(
                    text=f"{report.city} {report.date.day}.{report.date.month}.{report.date.year}",
                    callback_data=ReportsActionsCb(action="report", value=report.id).pack()
                )
            ]
        )
    current_page += 1
    button_page = InlineKeyboardButton(
        text=f"{current_page - 1}/{total_pages}",
        callback_data=ReportsActionsCb(action="None", value=0).pack()
    )
    button_next = InlineKeyboardButton(
        text=f"Вперед",
        callback_data=ReportsActionsCb(action="next", value=current_page).pack()
    )
    markup = InlineKeyboardMarkup(
        inline_keyboard=[*buttons, [button_page, button_next]]
    )

    await query.message.edit_text(
        text=text,
        reply_markup=markup
    )


@dp.callback_query(ReportsActionsCb.filter(F.action == "delete"))
async def callback_show_report(query: CallbackQuery, callback_data: CallbackData,
                               state: FSMContext):
    report_id = callback_data.value
    db_client.delete_user_report(report_id)

    current_page = 1
    await state.update_data(current_page=current_page)
    reports = db_client.get_user_reports(query.from_user.id)
    total_pages = math.ceil(len(reports) / 4)
    text = "История запросов:"
    buttons = []
    for report in reports[:current_page * 4]:
        buttons.append(
            [
                InlineKeyboardButton(
                    text=f"{report.city} {report.date.day}.{report.date.month}.{report.date.year}",
                    callback_data=ReportsActionsCb(action="report", value=report.id).pack()
                )
            ]
        )
    current_page += 1
    button_page = InlineKeyboardButton(
        text=f"{current_page - 1}/{total_pages}",
        callback_data=ReportsActionsCb(action="None", value=0).pack()
    )
    button_next = InlineKeyboardButton(
        text=f"Вперед",
        callback_data=ReportsActionsCb(action="next", value=current_page).pack()
    )
    markup = InlineKeyboardMarkup(
        inline_keyboard=[*buttons, [button_page, button_next]]
    )

    await query.message.edit_text(
        text=text,
        reply_markup=markup
    )


@dp.message(IsAdmin(), F.text == "Администратор")
async def admin_panel(message: Message):
    btn1 = KeyboardButton(text="Список пользователей")
    text = "Админ-панель"
    markup = ReplyKeyboardMarkup(keyboard=[[btn1]])
    await message.answer(
        text=text,
        reply_markup=markup
    )


@dp.message(IsAdmin(), F.text == "Список пользователей")
async def get_all_users(message: Message):
    current_page = 1
    users = db_client.get_all_users()
    total_pages = math.ceil(len(users) / 4)
    buttons = []
    for user in users[:current_page * 4]:
        conn_date = f"{user.connection_date.day}.{user.connection_date.month}.{user.connection_date.year}"
        buttons.append(
            [
                InlineKeyboardButton(
                    text=f"{user.id}) id: {user.tg_id}, подключился {conn_date}, {len(user.reports)} отчётов",
                    callback_data=AdminsActionsCb(action="None", value=0).pack()
                )
            ]
        )
    current_page += 1
    button_page = InlineKeyboardButton(
        text=f"{current_page - 1}/{total_pages}",
        callback_data=AdminsActionsCb(action="None", value=0).pack()
    )
    button_next = InlineKeyboardButton(
        text="Вперед",
        callback_data=AdminsActionsCb(action="next_users_page", value=current_page).pack()
    )
    markup = InlineKeyboardMarkup(
        inline_keyboard=[*buttons, [button_page, button_next]]
    )
    await message.answer(
        text="Все пользователи бота:",
        reply_markup=markup
    )


@dp.callback_query(AdminsActionsCb.filter(F.action == "next_users_page"))
async def callback_next_reports_page(query: CallbackQuery, callback_data: CallbackData,
                                     state: FSMContext):
    current_page = callback_data.value
    await state.update_data(current_page=current_page)
    users = db_client.get_all_users()
    total_pages = math.ceil(len(users) / 4)
    if current_page * 4 >= len(users):
        buttons = []
        for user in users[current_page * 4 - 4:len(users) + 1]:
            conn_date = f"{user.connection_date.day}.{user.connection_date.month}.{user.connection_date.year}"
            buttons.append(
                [
                    InlineKeyboardButton(
                        text=f"{user.id}) id: {user.tg_id}, подключился {conn_date}, {len(user.reports)} отчётов",
                        callback_data=AdminsActionsCb(action="None", value=0).pack()
                    )
                ]
            )
        current_page -= 1
        button_page = InlineKeyboardButton(
            text=f"{current_page + 1}/{total_pages}",
            callback_data=AdminsActionsCb(action="None", value=0).pack()
        )
        button_prev = InlineKeyboardButton(
            text="Назад",
            callback_data=AdminsActionsCb(action="prev_users_page", value=current_page).pack()
        )
        markup = InlineKeyboardMarkup(
            inline_keyboard=[*buttons, [button_prev, button_page]]
        )
        await query.message.edit_text(
            text="Все пользователи бота:",
            reply_markup=markup
        )
    else:
        buttons = []
        for user in users[current_page * 4 - 4:current_page * 4]:
            conn_date = f"{user.connection_date.day}.{user.connection_date.month}.{user.connection_date.year}"
            buttons.append(
                [
                    InlineKeyboardButton(
                        text=f"{user.id}) id: {user.tg_id}, подключился {conn_date}, {len(user.reports)} отчётов",
                        callback_data=AdminsActionsCb(action="None", value=0).pack()
                    )
                ]
            )
        current_page += 1
        button_prev = InlineKeyboardButton(
            text="Назад",
            callback_data=AdminsActionsCb(action="prev_users_page", value=current_page - 2).pack()
        )
        button_page = InlineKeyboardButton(
            text=f"{current_page - 1}/{total_pages}",
            callback_data=AdminsActionsCb(action="None", value=0).pack()
        )
        button_next = InlineKeyboardButton(
            text="Вперед",
            callback_data=AdminsActionsCb(action="next_users_page", value=current_page).pack()
        )
        markup = InlineKeyboardMarkup(
            inline_keyboard=[*buttons, [button_prev, button_page, button_next]]
        )
        await query.message.edit_text(
            text="Все пользователи бота:",
            reply_markup=markup
        )


@dp.callback_query(AdminsActionsCb.filter(F.action == "prev_users_page"))
async def callback_next_reports_page(query: CallbackQuery, callback_data: CallbackData,
                                     state: FSMContext):
    current_page = callback_data.value
    await state.update_data(current_page=current_page)
    users = db_client.get_all_users()
    total_pages = math.ceil(len(users) / 4)
    if current_page == 1:
        buttons = []
        for user in users[:current_page * 4]:
            conn_date = f"{user.connection_date.day}.{user.connection_date.month}.{user.connection_date.year}"
            buttons.append(
                [
                    InlineKeyboardButton(
                        text=f"{user.id}) id: {user.tg_id}, подключился {conn_date}, {len(user.reports)} отчётов",
                        callback_data=AdminsActionsCb(action="None", value=0).pack()
                    )
                ]
            )
        current_page += 1
        button_page = InlineKeyboardButton(
            text=f"{current_page - 1}/{total_pages}",
            callback_data=AdminsActionsCb(action="None", value=0).pack()
        )
        button_next = InlineKeyboardButton(
            text="Вперед",
            callback_data=AdminsActionsCb(action="next_users_page", value=current_page).pack()
        )
        markup = InlineKeyboardMarkup(
            inline_keyboard=[*buttons, [button_page, button_next]]
        )
        await query.message.edit_text(
            text="Все пользователи бота:",
            reply_markup=markup
        )
    else:
        buttons = []
        for user in users[current_page * 4 - 4:current_page * 4]:
            conn_date = f"{user.connection_date.day}.{user.connection_date.month}.{user.connection_date.year}"
            buttons.append(
                [
                    InlineKeyboardButton(
                        text=f"{user.id}) id: {user.tg_id}, подключился {conn_date}, {len(user.reports)} отчётов",
                        callback_data=AdminsActionsCb(action="None", value=0).pack()
                    )
                ]
            )
        current_page -= 1
        button_prev = InlineKeyboardButton(
            text="Назад",
            callback_data=AdminsActionsCb(action="prev_users_page", value=current_page).pack()
        )
        button_page = InlineKeyboardButton(
            text=f"{current_page + 1}/{total_pages}",
            callback_data=AdminsActionsCb(action="None", value=0).pack()
        )
        button_next = InlineKeyboardButton(
            text="Вперед",
            callback_data=AdminsActionsCb(action="next_users_page", value=current_page).pack()
        )
        markup = InlineKeyboardMarkup(
            inline_keyboard=[*buttons, [button_prev, button_page, button_next]]
        )
        await query.message.edit_text(
            text="Все пользователи бота:",
            reply_markup=markup
        )


if __name__ == '__main__':
    basicConfig(level=INFO)
    db_client.create_tables()
    dp.run_polling(bot, skip_updates=True)
