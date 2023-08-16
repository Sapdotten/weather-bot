from aiogram import Dispatcher, types
from aiogram.dispatcher.filters.builtin import CommandStart
import texts as tx
from handlers.machine_states import CityState
from data_manager import data_manager as db
from aiogram.dispatcher import FSMContext
from modules.weather_parser import city_exists
from keyboards.reply_keyboards import std_keyboard
from keyboards.timepicker import TimePicker, TimeFilter
from modules.scheduler import cancel


async def start(msg: types.Message):
    """отвечает на /start"""
    await msg.answer(text=tx.START1)
    await msg.answer(text=tx.START2)
    await CityState.city.set()


async def get_city(msg: types.Message, state: FSMContext):
    """Получает город пользователя"""
    msg_city = msg.text
    city = await city_exists(msg_city)
    if not city:
        await msg.answer(tx.ERROR_CITY.substitute(city=msg_city))
    else:
        await db.add_user(msg.from_id, city[1], city[0], city[2])
        await msg.answer(text=tx.SAVE_CITY.substitute(city=city[1]), reply_markup=std_keyboard())
        await state.finish()


async def get_time(msg: types.Message):
    """Позволяет изменить время рассылки"""
    await msg.answer(text=tx.TO_CHANGE_TIME, reply_markup=await TimePicker.start())


async def get_time_proc(cbq: types.CallbackQuery):
    """Получает время, введенное пользователем"""
    time = await TimePicker.process_data(cbq)
    print(f'set_time {time}')
    await cbq.message.answer(text=tx.CHANGED_TIME.substitute(time=time))
    old_time = await db.get_time_server(cbq.from_user.id)
    await db.set_time(cbq.from_user.id, time)
    time = await db.get_time_server(cbq.from_user.id)
    await cancel(cbq.bot, old_time, time)


async def change_city(msg: types.Message):
    await CityState.city.set()
    await msg.answer(text=tx.TO_CHANGE_CITY)


def register(dp: Dispatcher):
    dp.register_message_handler(start, CommandStart(), content_types='text')
    dp.register_message_handler(get_city, state=CityState.city)
    dp.register_message_handler(get_time, content_types='text', text='Изменить время рассылки')
    dp.register_callback_query_handler(get_time_proc, TimeFilter())
    dp.register_message_handler(change_city, content_types='text', text='Изменить город')
