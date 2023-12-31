from aiogram import types, Bot
import texts as tx
from handlers.machine_states import CityState
from data import data_manager as db
from aiogram.fsm.context import FSMContext
from modules.weather_parser import city_exists
from keyboards.reply_keyboards import std_keyboard
from keyboards.timepicker import TimePicker, TimeFilter
from modules.scheduler import cancel
from aiogram.dispatcher.router import Router
from aiogram.filters import Command
from aiogram import F
import logging
from modules.user_manager import User
from modules.weather_manager import Weather

command_router = Router()
bot: Bot


@command_router.message(Command(commands=["start"]))
async def start(msg: types.Message, state: FSMContext):
    """отвечает на /start"""
    await msg.answer(text=tx.START1)
    await msg.answer(text=tx.START2)
    await state.set_state(CityState.city)


@command_router.message(CityState.city)
async def get_city(msg: types.Message, state: FSMContext):
    """Получает город пользователя"""
    is_city = await User.add_user(msg.from_user.id, msg.text)
    if not is_city:
        await msg.answer(tx.ERROR_CITY.substitute(city=msg.text))
    else:
        await msg.answer(text=tx.SAVE_CITY.substitute(city=is_city), reply_markup=std_keyboard())
        await state.clear()


@command_router.message(F.text == 'Изменить время рассылки')
async def change_time(msg: types.Message):
    """Позволяет изменить время рассылки"""
    await msg.answer(text=tx.TO_CHANGE_TIME, reply_markup=await TimePicker.start())


@command_router.callback_query(TimeFilter())
async def get_time(cbq: types.CallbackQuery):
    """Получает время, введенное пользователем"""
    time = await TimePicker.process_data(cbq)
    await cbq.message.answer(text=tx.CHANGED_TIME.substitute(time=time))
    old_time = await db.get_time_server(cbq.from_user.id)
    await db.set_time(cbq.from_user.id, time)
    time = await db.get_time_server(cbq.from_user.id)
    if await db.get_auto_send_status(cbq.from_user.id):
        await cancel(old_time, time)


@command_router.message(F.text == 'Изменить город')
async def change_city(msg: types.Message, state: FSMContext):
    await state.set_state(CityState.city)
    await msg.answer(text=tx.TO_CHANGE_CITY)


@command_router.message(Command(commands=["switcher"]))
async def switcher(msg: types.Message):
    status = await db.get_auto_send_status(msg.from_user.id)
    await db.set_auto_send_status(msg.from_user.id, not status)
    if status:
        await msg.answer(text=tx.CHANGED_AUTO_SEND.substitute(status='отключена'))
    else:
        await msg.answer(text=tx.CHANGED_AUTO_SEND.substitute(status='включена'))
        time = await db.get_time_server(msg.from_user.id)
        await cancel(time, time)


@command_router.message(Command(commands=["report"]))
async def report(msg: types.Message):
    if msg.from_user.id == 859743151:
        await msg.answer(text=f'Пользователей в базе данных: {await db.get_count_of_users()}')


@command_router.message(Command(commands=['get_db']))
async def get_db(msg: types.Message):
    if msg.from_user.id == 859743151:
        await msg.answer(text=str(await db.get_users()))
