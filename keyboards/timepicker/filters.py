from aiogram.dispatcher.filters import BoundFilter
from aiogram import types
from keyboards.timepicker.time_keyboard import TimePicker, TimeCallback


class TimeFilter(BoundFilter):
    async def check(self, cbq: types.CallbackQuery):
        if not cbq.data.startswith('time:'):
            return False
        data = TimeCallback.deparse(cbq['data'])
        if data['num'] == '':
            await cbq.answer()
            return False
        if data['type'] == 'hour':
            await cbq.message.edit_reply_markup(reply_markup=TimePicker.get_minutes(data['num']))
            return False
        elif data['type'] == 'minute':
            await cbq.message.delete()
            return True

