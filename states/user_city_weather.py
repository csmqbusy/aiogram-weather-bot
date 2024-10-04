from aiogram.fsm.state import StatesGroup, State


class SetUserCity(StatesGroup):
    waiting_city = State()
