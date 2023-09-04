# -*- coding: utf-8 -*-
from aiogram import types
import texts as tx
from data import data_manager as dm
from modules.weather_parser import get_weather_now, get_weather
from modules.get_clothes import what_to_wear as cloth
from keyboards.reply_keyboards import std_keyboard
from aiogram.dispatcher.router import Router
from aiogram import F

wearing_router = Router()


@wearing_router.message(F.text == 'Что надеть сейчас?')
async def what_to_wear_now(msg: types.Message):
    print('Что надеть сейчас?')
    city = await dm.get_city(msg.from_user.id)
    if city is not None:
        weather = await get_weather_now(city['id'])
        await msg.answer(text=tx.WEATHER_NOW.substitute(city_name=city['name'],
                                                        temp=weather['temp'],
                                                        descr=weather['descr']))
        dress = await cloth(weather['comfort'], weather['descr'])
        await msg.answer(text=dress, reply_markup=std_keyboard())
        if msg.from_user.id == 1161728791:
            await msg.answer(text='Сань, иди нахуй)')


@wearing_router.message(F.text == 'Что надеть сегодня?')
async def what_to_wear_today(msg: types.Message):
    print('Что надеть сегодня?')
    city = await dm.get_city(msg.from_user.id)
    if city is not None:
        weather = await get_weather(city['id'], 0)
        await msg.answer(text=tx.WEATHER_DAY.substitute(city_name=city['name'],
                                                        day='Сегодня',
                                                        max_t=weather['max_t'],
                                                        min_t=weather['min_t'],
                                                        descr=weather['descr']))
        dress = await cloth(weather['comfort'], weather['descr'])
        await msg.answer(text=dress, reply_markup=std_keyboard())
        if msg.from_user.id == 1161728791:
            await msg.answer(text='Сань, иди нахуй)')


@wearing_router.message(F.text == 'Что надеть завтра?')
async def what_to_wear_tomorrow(msg: types.Message):
    print('Что надеть завтра?')
    city = await dm.get_city(msg.from_user.id)
    if city is not None:
        weather = await get_weather(city['id'], 1)
        await msg.answer(text=tx.WEATHER_DAY.substitute(city_name=city['name'],
                                                        day='Завтра',
                                                        max_t=weather['max_t'],
                                                        min_t=weather['min_t'],
                                                        descr=weather['descr']))
        dress = await cloth(weather['comfort'], weather['descr'])
        await msg.answer(text=dress, reply_markup=std_keyboard())
        if msg.from_user.id == 1161728791:
            await msg.answer(text='Сань, иди нахуй)')

# def register_wearing(dp: Dispatcher) -> None:
#     dp.message.register(what_to_wear_today, content_types='text', text='Что надеть?')
