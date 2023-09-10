# -*- coding: utf-8 -*-
from aiogram import types
import texts as tx
from data import data_manager as dm
from modules.weather_parser import get_weather_now, get_weather
import modules.get_clothes_new as cloth
from keyboards.reply_keyboards import std_keyboard
from aiogram.dispatcher.router import Router
from aiogram import F
import logging

wearing_router = Router()


@wearing_router.message(F.text == 'Что надеть сейчас?')
async def what_to_wear_now(msg: types.Message):
    logging.info('What to wear now', {id: msg.from_user.id})
    city = await dm.get_city(msg.from_user.id)
    if city is not None:
        weather = await get_weather_now(city['id'])
        await msg.answer(text=tx.WEATHER_NOW.substitute(city_name=city['name'],
                                                        temp=weather['temp'],
                                                        descr=weather['descr']))
        logging.info('comfort t is %s', weather['comfort'])
        dress = await cloth.get_clothes(weather['comfort'], weather['descr'])
        await msg.answer(text=dress, reply_markup=std_keyboard())
        if msg.from_user.id == 1161728791:
            await msg.answer(text='Сань, иди нахуй)')


@wearing_router.message(F.text == 'Что надеть сегодня?')
async def what_to_wear_today(msg: types.Message):
    logging.info('What to wear today', {id: msg.from_user.id})
    city = await dm.get_city(msg.from_user.id)
    if city is not None:
        weather = await get_weather(city['id'], 0)
        await msg.answer(text=tx.WEATHER_DAY.substitute(city_name=city['name'],
                                                        day='Сегодня',
                                                        max_t=weather['max_t'],
                                                        min_t=weather['min_t'],
                                                        descr=weather['descr']))
        logging.info('comfort t is %s', weather['comfort'])
        dress = await cloth.get_clothes(weather['comfort'], weather['descr'])
        await msg.answer(text=dress, reply_markup=std_keyboard())
        if msg.from_user.id == 1161728791:
            await msg.answer(text='Сань, иди нахуй)')


@wearing_router.message(F.text == 'Что надеть завтра?')
async def what_to_wear_tomorrow(msg: types.Message):
    logging.info('What to wear tomorrow', {id: msg.from_user.id})
    city = await dm.get_city(msg.from_user.id)
    if city is not None:
        weather = await get_weather(city['id'], 1)
        await msg.answer(text=tx.WEATHER_DAY.substitute(city_name=city['name'],
                                                        day='Завтра',
                                                        max_t=weather['max_t'],
                                                        min_t=weather['min_t'],
                                                        descr=weather['descr']))
        dress = await cloth.get_clothes(weather['comfort'], weather['descr'])
        await msg.answer(text=dress, reply_markup=std_keyboard())
        if msg.from_user.id == 1161728791:
            await msg.answer(text='Сань, иди нахуй)')

# def register_wearing(dp: Dispatcher) -> None:
#     dp.message.register(what_to_wear_today, content_types='text', text='Что надеть?')
