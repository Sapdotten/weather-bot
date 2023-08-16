from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def std_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='Что надеть?')],
        [KeyboardButton(text='Изменить время рассылки')],
        [KeyboardButton(text='Изменить город')]
    ], resize_keyboard=True, one_time_keyboard=True)
