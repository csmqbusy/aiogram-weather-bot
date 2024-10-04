import math

from aiogram import F, Router
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

from database.orm import db_client
from filters import IsAdmin

router = Router()
router.message.filter(IsAdmin())
router.callback_query.filter(IsAdmin())


class AdminsActionsCb(CallbackData, prefix='admins_actions'):
    action: str


@router.message(F.text == "Список пользователей")
async def get_all_users(message: Message, state: FSMContext):
    current_page = 1
    await state.update_data(current_page=current_page)
    users = db_client.get_all_users()
    total_pages = math.ceil(len(users) / 4)
    buttons = []
    for user in users[:current_page * 4]:
        conn_date = f"{user.connection_date.day}.{user.connection_date.month}.{user.connection_date.year}"
        buttons.append(
            [
                InlineKeyboardButton(
                    text=f"{user.id}) id: {user.tg_id}, подключился {conn_date}, {len(user.reports)} отчётов",
                    callback_data=AdminsActionsCb(action="None").pack()
                )
            ]
        )
    button_page = InlineKeyboardButton(
        text=f"{current_page}/{total_pages}",
        callback_data=AdminsActionsCb(action="None").pack()
    )
    button_next = InlineKeyboardButton(
        text="Вперед",
        callback_data=AdminsActionsCb(action="next_users_page").pack()
    )
    markup = InlineKeyboardMarkup(
        inline_keyboard=[*buttons, [button_page, button_next]]
    )
    await message.answer(
        text="Все пользователи бота:",
        reply_markup=markup
    )


@router.callback_query(AdminsActionsCb.filter(F.action == "next_users_page"))
async def callback_next_reports_page(query: CallbackQuery, callback_data: CallbackData,
                                     state: FSMContext):
    current_page = (await state.get_data()).get("current_page")
    current_page += 1
    await state.update_data(current_page=current_page)
    users = db_client.get_all_users()
    total_pages = math.ceil(len(users) / 4)
    if current_page * 4 >= len(users):  # если эта страница последняя
        buttons = []
        for user in users[current_page * 4 - 4:len(users) + 1]:  # if len=10 [12 - 4:10+1]
            conn_date = f"{user.connection_date.day}.{user.connection_date.month}.{user.connection_date.year}"
            buttons.append(
                [
                    InlineKeyboardButton(
                        text=f"{user.id}) id: {user.tg_id}, подключился {conn_date}, {len(user.reports)} отчётов",
                        callback_data=AdminsActionsCb(action="None").pack()
                    )
                ]
            )
        button_page = InlineKeyboardButton(
            text=f"{current_page}/{total_pages}",
            callback_data=AdminsActionsCb(action="None").pack()
        )
        button_prev = InlineKeyboardButton(
            text="Назад",
            callback_data=AdminsActionsCb(action="prev_users_page").pack()
        )
        markup = InlineKeyboardMarkup(
            inline_keyboard=[*buttons, [button_prev, button_page]]
        )
        await query.message.edit_text(
            text="Все пользователи бота:",
            reply_markup=markup
        )
    else:  # если эта страница не последняя
        buttons = []
        for user in users[current_page * 4 - 4:current_page * 4]:
            conn_date = f"{user.connection_date.day}.{user.connection_date.month}.{user.connection_date.year}"
            buttons.append(
                [
                    InlineKeyboardButton(
                        text=f"{user.id}) id: {user.tg_id}, подключился {conn_date}, {len(user.reports)} отчётов",
                        callback_data=AdminsActionsCb(action="None").pack()
                    )
                ]
            )
        button_prev = InlineKeyboardButton(
            text="Назад",
            callback_data=AdminsActionsCb(action="prev_users_page").pack()
        )
        button_page = InlineKeyboardButton(
            text=f"{current_page}/{total_pages}",
            callback_data=AdminsActionsCb(action="None").pack()
        )
        button_next = InlineKeyboardButton(
            text="Вперед",
            callback_data=AdminsActionsCb(action="next_users_page").pack()
        )
        markup = InlineKeyboardMarkup(
            inline_keyboard=[*buttons, [button_prev, button_page, button_next]]
        )
        await query.message.edit_text(
            text="Все пользователи бота:",
            reply_markup=markup
        )


@router.callback_query(AdminsActionsCb.filter(F.action == "prev_users_page"))
async def callback_prev_reports_page(query: CallbackQuery, callback_data: CallbackData,
                                     state: FSMContext):
    current_page = (await state.get_data()).get("current_page")
    current_page -= 1
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
                        callback_data=AdminsActionsCb(action="None").pack()
                    )
                ]
            )
        button_page = InlineKeyboardButton(
            text=f"{current_page}/{total_pages}",
            callback_data=AdminsActionsCb(action="None").pack()
        )
        button_next = InlineKeyboardButton(
            text="Вперед",
            callback_data=AdminsActionsCb(action="next_users_page").pack()
        )
        markup = InlineKeyboardMarkup(
            inline_keyboard=[*buttons, [button_page, button_next]]
        )
        await query.message.edit_text(
            text="Все пользователи бота:",
            reply_markup=markup
        )
    else:  # если страница не первая
        buttons = []
        for user in users[current_page * 4 - 4:current_page * 4]:
            conn_date = f"{user.connection_date.day}.{user.connection_date.month}.{user.connection_date.year}"
            buttons.append(
                [
                    InlineKeyboardButton(
                        text=f"{user.id}) id: {user.tg_id}, подключился {conn_date}, {len(user.reports)} отчётов",
                        callback_data=AdminsActionsCb(action="None").pack()
                    )
                ]
            )
        button_prev = InlineKeyboardButton(
            text="Назад",
            callback_data=AdminsActionsCb(action="prev_users_page").pack()
        )
        button_page = InlineKeyboardButton(
            text=f"{current_page}/{total_pages}",
            callback_data=AdminsActionsCb(action="None").pack()
        )
        button_next = InlineKeyboardButton(
            text="Вперед",
            callback_data=AdminsActionsCb(action="next_users_page").pack()
        )
        markup = InlineKeyboardMarkup(
            inline_keyboard=[*buttons, [button_prev, button_page, button_next]]
        )
        await query.message.edit_text(
            text="Все пользователи бота:",
            reply_markup=markup
        )
