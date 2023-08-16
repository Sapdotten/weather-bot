# -*- coding: utf-8 -*-
from aiogram import Dispatcher, types
import texts as tx
from data_manager import data_manager as dm
from modules.weather_parser import get_weather
from modules.get_clothes import what_to_wear as cloth
from keyboards.reply_keyboards import std_keyboard


# from weather_parser import


async def what_to_wear_today(msg: types.Message):
    print('Что надеть?')
    city = await dm.get_city(msg.from_id)
    if city is not None:
        weather = await get_weather(city['id'])
        await msg.answer(text=tx.WEATHER_TODAY.substitute(city_name=city['name'],
                                                          max_t=weather['max_t'],
                                                          min_t=weather['min_t'],
                                                          descr=weather['descr']))
        dress = await cloth(weather['comfort'], weather['descr'])
        await msg.answer(text=dress, reply_markup=std_keyboard())
        if msg.from_id == 1161728791:
            await msg.answer(text = 'Сань, иди нахуй)')


def register_wearing(dp: Dispatcher) -> None:
    dp.register_message_handler(what_to_wear_today, content_types='text', text='Что надеть?')
