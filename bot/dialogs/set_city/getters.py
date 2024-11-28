from aiogram_dialog import DialogManager


async def get_user_city_from_state(
        dialog_manager: DialogManager,
        **kwargs,
) -> dict[str, str | None]:
    user_city = dialog_manager.dialog_data.get("user_city")
    return {"user_city": user_city}
