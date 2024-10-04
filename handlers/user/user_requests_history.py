import math

from aiogram import F, Router
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

from database.orm import db_client

router = Router()


class ReportsActionsCb(CallbackData, prefix='reports_actions'):
    action: str
    value: int


@router.message(F.text == "История")
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


@router.callback_query(ReportsActionsCb.filter(F.action == "next"))
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


@router.callback_query(ReportsActionsCb.filter(F.action == "prev"))
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


@router.callback_query(ReportsActionsCb.filter(F.action == "report"))
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


@router.callback_query(F.data == "back_to_history")
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


@router.callback_query(ReportsActionsCb.filter(F.action == "delete"))
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
