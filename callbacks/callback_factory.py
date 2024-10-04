from aiogram.filters.callback_data import CallbackData


class AdminsActionsCb(CallbackData, prefix="admins_actions"):
    action: str
