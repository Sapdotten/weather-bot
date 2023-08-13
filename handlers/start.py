from aiogram import Dispatcher, types
from aiogram.dispatcher.filters.builtin import CommandStart
import texts as tx
from handlers.machine_states import CityState
from data_manager import data_manager as dm
from aiogram.dispatcher import FSMContext
from weather_parser import city_exists
from keyboards.reply_keyboards import what_to_wear_rkb


async def start(msg: types.Message):
    await msg.answer(text=tx.START)
    await CityState.city.set()


async def get_city(msg: types.Message, state: FSMContext):
    msg_city = msg.text
    city = await city_exists(msg_city)
    if not city:
        await msg.answer(tx.ERROR_CITY.substitute(city=msg_city))
    else:
        await dm.add_user(msg.from_id, city[1], city[0])
        await msg.answer(text=tx.SAVE_CITY.substitute(city=city[1]), reply_markup=what_to_wear_rkb())
        await state.finish()


def register(dp: Dispatcher):
    dp.register_message_handler(start, CommandStart(), content_types='text')
    dp.register_message_handler(get_city, state=CityState.city)
