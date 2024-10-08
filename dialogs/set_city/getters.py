from aiogram_dialog import DialogManager


async def get_user_city(dialog_manager: DialogManager, **kwargs):
    user_city = dialog_manager.dialog_data.get("user_city")
    return {"user_city": user_city}
