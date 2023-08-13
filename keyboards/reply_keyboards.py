from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def what_to_wear_rkb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='Что надеть?')]
    ], resize_keyboard=True, one_time_keyboard=True)
