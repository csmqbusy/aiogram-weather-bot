import math

from aiogram import F, Router
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from callbacks import ReportsActionsCb, ReportViewCb
from database.orm import db_client
from keyboards.inline.report_view import report_view_kb
from keyboards.inline.user_history_nav import reports_history_kb

router = Router()


@router.callback_query(F.data == "back_to_history")
@router.message(F.text == "История")
async def show_reports_first_page(update: Message | CallbackQuery, state: FSMContext):
    current_page = 1
    await state.update_data(current_page=current_page)
    reports = db_client.get_user_reports(update.from_user.id)
    total_pages = math.ceil(len(reports) / 4)
    curr_page_text = f"{current_page}/{total_pages}"
    markup = reports_history_kb(
        reports=reports, slice_=slice(current_page * 4),
        curr_page_text=curr_page_text, next_=True
    )
    text = "История запросов:"
    if hasattr(update, "data"):
        await update.message.edit_text(
            text=text,
            reply_markup=markup
        )
    else:
        await update.answer(
            text=text,
            reply_markup=markup
        )


@router.callback_query(ReportsActionsCb.filter(F.action == "next"))
async def callback_next_reports_page(query: CallbackQuery, state: FSMContext):
    current_page = (await state.get_data()).get("current_page")
    current_page += 1
    await state.update_data(current_page=current_page)
    reports = db_client.get_user_reports(query.from_user.id)
    total_pages = math.ceil(len(reports) / 4)
    curr_page_text = f"{current_page}/{total_pages}"
    if current_page * 4 >= len(reports):
        slice_ = slice(current_page * 4 - 4, len(reports) + 1)
        next_ = False
    else:
        slice_ = slice(current_page * 4 - 4, current_page * 4)
        next_ = True
    markup = reports_history_kb(
        reports=reports, slice_=slice_,
        curr_page_text=curr_page_text, prev=True, next_=next_
    )
    await query.message.edit_text(
        text="История запросов:",
        reply_markup=markup
    )


@router.callback_query(ReportsActionsCb.filter(F.action == "prev"))
async def callback_prev_reports_page(query: CallbackQuery, state: FSMContext):
    current_page = (await state.get_data()).get("current_page")
    current_page -= 1
    await state.update_data(current_page=current_page)
    reports = db_client.get_user_reports(query.from_user.id)
    total_pages = math.ceil(len(reports) / 4)
    curr_page_text = f"{current_page}/{total_pages}"
    if current_page == 1:
        slice_ = slice(current_page * 4)
        prev = False
    else:
        slice_ = slice(current_page * 4 - 4, current_page * 4)
        prev = True
    markup = reports_history_kb(
        reports=reports, slice_=slice_,
        curr_page_text=curr_page_text, prev=prev, next_=True
    )
    await query.message.edit_text(
        text="История запросов:",
        reply_markup=markup
    )


@router.callback_query(ReportViewCb.filter(F.action == "show"))
async def callback_show_report(query: CallbackQuery, callback_data: CallbackData):
    report_id = callback_data.report_id
    reports = db_client.get_user_reports(query.from_user.id)
    current_report = None
    for report in reports:
        if report.id == report_id:
            current_report = report
            break
    markup = report_view_kb(report_id)
    text = ("Данные по запросу:\n\n"
            f"Город: {current_report.city}\n"
            f"Температура: {current_report.temp} °C\n"
            f"Ощущается как: {current_report.feels_like} °C\n"
            f"Скорость ветра: {current_report.wind_speed} км/ч\n"
            f"Давление: {current_report.pressure_mm} мм рт. ст.")
    await query.message.edit_text(
        text=text,
        reply_markup=markup
    )


@router.callback_query(ReportViewCb.filter(F.action == "delete"))
async def callback_delete_report(query: CallbackQuery, callback_data: CallbackData,
                                 state: FSMContext):
    report_id = callback_data.report_id
    db_client.delete_user_report(report_id)

    await show_reports_first_page(query, state)
