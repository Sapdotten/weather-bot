from aiogram.dispatcher.filters.state import StatesGroup, State


class CityState(StatesGroup):
    city = State()
