from aiogram.fsm.state import StatesGroup, State


class AdminMenuSG(StatesGroup):
    main = State()


class UsersListSG(StatesGroup):
    main = State()


class UserMenuSG(StatesGroup):
    main = State()


class MyCityWeatherSG(StatesGroup):
    main = State()


class OtherCityWeatherSG(StatesGroup):
    city_selection = State()
    weather = State()


class RequestsHistorySG(StatesGroup):
    main = State()


class SetCitySG(StatesGroup):
    setup_city = State()
    city_accepted = State()
