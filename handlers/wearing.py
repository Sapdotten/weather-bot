# -*- coding: utf-8 -*-
from aiogram import Dispatcher, types
import texts as tx
from data_manager import data_manager as dm
from weather_parser import get_weather


# from weather_parser import


async def what_to_wear(msg: types.Message):
    city = await dm.get_city(msg.from_id)
    if city is None:
        return 0
    weather = await get_weather(city['id'])
    await msg.answer(text=tx.WEATHER_TODAY.substitute(user_name=msg.from_user.first_name,
                                                      city_name=city['name'],
                                                      max_t=weather['max_t'],
                                                      min_t=weather['min_t'],
                                                      descr=weather['descr']))


def register_wearing(dp: Dispatcher) -> None:
    dp.register_message_handler(what_to_wear, content_types='text', text='Что надеть?')
