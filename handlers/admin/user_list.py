import math

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from callbacks import AdminsActionsCb
from database.orm import db_client
from filters import IsAdmin
from keyboards.inline.admin_userlist_nav import userlist_kb

router = Router()
router.message.filter(IsAdmin())
router.callback_query.filter(IsAdmin())


@router.message(F.text == "Список пользователей")
async def get_all_users(message: Message, state: FSMContext):
    current_page = 1
    await state.update_data(current_page=current_page)
    users = db_client.get_all_users()
    total_pages = math.ceil(len(users) / 4)
    curr_page_text = f"{current_page}/{total_pages}"
    markup = userlist_kb(
        users=users, slice_=slice(current_page * 4),
        curr_page_text=curr_page_text, next_=True
    )
    await message.answer(
        text="Все пользователи бота:",
        reply_markup=markup
    )


@router.callback_query(AdminsActionsCb.filter(F.action == "next_users_page"))
async def callback_next_reports_page(query: CallbackQuery, state: FSMContext):
    current_page = (await state.get_data()).get("current_page")
    current_page += 1
    await state.update_data(current_page=current_page)
    users = db_client.get_all_users()
    total_pages = math.ceil(len(users) / 4)
    curr_page_text = f"{current_page}/{total_pages}"
    if current_page * 4 >= len(users):
        markup = userlist_kb(
            users=users, slice_=slice(current_page * 4 - 4, len(users) + 1),
            curr_page_text=curr_page_text, prev=True
        )
    else:
        markup = userlist_kb(
            users=users, slice_=slice(current_page * 4 - 4, current_page * 4),
            curr_page_text=curr_page_text, prev=True, next_=True
        )
    await query.message.edit_text(
        text="Все пользователи бота:",
        reply_markup=markup
    )


@router.callback_query(AdminsActionsCb.filter(F.action == "prev_users_page"))
async def callback_prev_reports_page(query: CallbackQuery, state: FSMContext):
    current_page = (await state.get_data()).get("current_page")
    current_page -= 1
    await state.update_data(current_page=current_page)
    users = db_client.get_all_users()
    total_pages = math.ceil(len(users) / 4)
    curr_page_text = f"{current_page}/{total_pages}"
    if current_page == 1:
        markup = userlist_kb(
            users=users, slice_=slice(current_page * 4),
            curr_page_text=curr_page_text, next_=True
        )
    else:
        markup = userlist_kb(
            users=users, slice_=slice(current_page * 4 - 4, current_page * 4),
            curr_page_text=curr_page_text, prev=True, next_=True
        )
    await query.message.edit_text(
        text="Все пользователи бота:",
        reply_markup=markup
    )
