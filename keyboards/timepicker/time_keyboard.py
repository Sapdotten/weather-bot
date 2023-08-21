from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData
from typing import List
from aiogram import types


class cb_data(CallbackData, prefix = 'time'):
    type: str
    num: str
    data: str


class TimeCallback:
    args: tuple[str] = ('time', 'type', 'num', 'data')
    # cb_data: CallbackData = CallbackData('time', 'type', 'num', 'data')
    data: str

    def __init__(self, data):
        self.data = data

    def get_data(self, type: str, num: str) -> str:
        return cb_data(type=type, num=num, data=self.data).pack()

    @classmethod
    def deparse(cls, data: str) -> dict[str, str]:
        data = data.split(':')
        res = {}
        for i in range(0, len(cls.args)):
            res[cls.args[i]] = data[i]
        return res


class Buttons:
    cb: TimeCallback

    def __init__(self, data: str):
        self.cb = TimeCallback(data)

    def get_button(self, text: str, type: str, cb_data: str) -> InlineKeyboardButton:
        """
        Возвращает Inline кнопку
        :param text: текст кнопки
        :param type: тип клавиатуры 'hour' или 'minute'
        :param cb_data: данные, которые вернет кнопка
        :param data: данные, сохраненные ранее
        :return: кнопка
        """
        return InlineKeyboardButton(text=text, callback_data=self.cb.get_data(type, cb_data))

    def get_markup(self, type: str, buttons: List[List[str]]) -> InlineKeyboardMarkup:
        list_of_lines = []
        for string in buttons:
            list_of_btns = []
            for btn in string:
                cbq = btn
                if not btn.isdigit():
                    cbq = ''
                list_of_btns.append(self.get_button(btn, type, cbq))
            list_of_lines.append(list_of_btns)
        return InlineKeyboardMarkup(inline_keyboard=list_of_lines,
                                    one_time_keyboard=True,
                                    resize=True)


class TimePicker:
    cb_data_h = 'hour'
    cb_data_m = 'minute'
    TimeCallback = cb_data

    @classmethod
    def bt_h(cls, hour: str):
        return InlineKeyboardButton(text=hour, callback_data=cls.TimeCallback(type='hour', num=hour).pack())

    @classmethod
    def bt_m(cls, _min: str):
        return InlineKeyboardButton(text=_min, callback_data=cls.cb_data_m + _min)

    @classmethod
    async def start(cls) -> InlineKeyboardMarkup:
        btn = Buttons('')
        return btn.get_markup('hour',
                              [['Select an hour'],
                               ['21', '22', '23', '00', '1', '2', '3'],
                               ['20', ' ', ' ', ' ', ' ', ' ', '4'],
                               ['19', ' ', ' ', ' ', ' ', ' ', '5'],
                               ['18', ' ', ' ', 'o', ' ', ' ', '6'],
                               ['17', ' ', ' ', ' ', ' ', ' ', '7'],
                               ['16', ' ', ' ', ' ', ' ', ' ', '8'],
                               ['15', '14', '13', '12', '11', '10', '9']
                               ])

    @classmethod
    def get_minutes(cls, hours: str) -> InlineKeyboardMarkup:
        btn = Buttons(hours)
        return btn.get_markup('minute',
                              [['Select a minute'],
                               [' ', '55', '00', '05', ' '],
                               ['50', ' ', ' ', ' ', '10'],
                               ['45', ' ', ' ', ' ', '15'],
                               ['40', ' ', ' ', ' ', '20'],
                               [' ', '35', '30', '25', ' ']
                               ])

    @classmethod
    async def process_data(cls, cb: types.CallbackQuery) -> str:
        cb = TimeCallback.deparse(cb.data)
        time = cb['data'] + ':' + cb['num']
        return time
