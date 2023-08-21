from aiogram.fsm.state import State, StatesGroup


class CityState(StatesGroup):
    city = State()
