from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def std_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='Что надеть сегодня?')],
        [KeyboardButton(text='Что надеть сейчас?')],
        [KeyboardButton(text='Что надеть завтра?')],
        [KeyboardButton(text='Изменить время рассылки')],
        [KeyboardButton(text='Изменить город')]
    ], resize_keyboard=True, one_time_keyboard=True)
