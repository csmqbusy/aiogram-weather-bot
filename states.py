from aiogram.fsm.state import StatesGroup, State


class AdminMenuSG(StatesGroup):
    main = State()


class UsersListSG(StatesGroup):
    main = State()
