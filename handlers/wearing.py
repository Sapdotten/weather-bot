# -*- coding: utf-8 -*-
from aiogram import Dispatcher, types
import texts as tx
from data_manager import data_manager as dm
from weather_parser import get_weather
from clothes import what_to_wear as cloth


# from weather_parser import


async def what_to_wear(msg: types.Message):
    city = await dm.get_city(msg.from_id)
    if city is not None:
        weather = await get_weather(city['id'])
        await msg.answer(text=tx.WEATHER_TODAY.substitute(city_name=city['name'],
                                                          max_t=weather['max_t'],
                                                          min_t=weather['min_t'],
                                                          descr=weather['descr']))
        dress = await cloth(weather['comfort'], weather['descr'])
        await msg.answer(text=dress)


def register_wearing(dp: Dispatcher) -> None:
    dp.register_message_handler(what_to_wear, content_types='text', text='Что надеть?')
