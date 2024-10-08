from aiogram.fsm.state import StatesGroup, State


class OtherCityWeather(StatesGroup):
    waiting_city = State()
