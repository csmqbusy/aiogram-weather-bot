import math

from aiogram_dialog import DialogManager

from database.orm import db_client


async def get_users_data(dialog_manager: DialogManager, **kwargs):
    users_orm = db_client.get_all_users()
    users = prepare_users_for_dialog(users_orm)
    n_items_per_page = 5
    n_of_users = len(users)
    current_page = dialog_manager.start_data.get("page")
    n_of_pages = math.ceil(n_of_users / n_items_per_page)
    slice_ = slice(current_page * n_items_per_page,
                   current_page * n_items_per_page + n_items_per_page)
    dialog_manager.start_data.update(n_of_pages=n_of_pages)
    return {
        "users": users[slice_],
        "count": n_of_users,
        "page": current_page + 1,
        "n_of_pages": n_of_pages
    }


def prepare_users_for_dialog(users_orm: list):
    users = []
    for user in users_orm:
        conn_date = f"{user.connection_date.day}.{user.connection_date.month}.{user.connection_date.year}"
        user_info = (user.id, user.tg_id, conn_date, len(user.reports))
        users.append(user_info)
    return sorted(users, key=lambda item: item[0])
