from modules.weather_parser import get_weather
from modules.get_clothes_new import get_clothes as what_to_wear
import texts as tx
from aiogram import Bot
import data.data_manager as db
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import logging

sched: AsyncIOScheduler


async def mail_by_city(bot: Bot, ids: list[list[int]], city_id: int, city_name: str) -> None:
    logging.info('start of mail by city', {'city': city_name})
    weather = await get_weather(city_id, day=0)
    text1 = tx.WEATHER_DAY.substitute(day='Сегодня',
                                      city_name=city_name,
                                      max_t=weather['max_t'],
                                      min_t=weather['min_t'],
                                      descr=weather['descr'])
    text2 = await what_to_wear(weather['comfort'], weather['descr'])
    for id in ids:
        await bot.send_message(chat_id=id[0], text=text1)
        await bot.send_message(chat_id=id[0], text=text2)


async def mail(bot: Bot, time: str) -> None:
    logging.info('start of mail by time', {'time': time})
    cities = await db.get_cities_with_time(time)
    for city in cities:
        print(f'город: {city[0], city[1]}')
        users = await db.get_users_with_time_city(time, city[0])
        await mail_by_city(bot, users, city[0], city[1])


async def scheduler(bot: Bot, times: list[list[str]]) -> None:
    global sched
    logging.info('start of scheduler')
    for time in times:
        logging.info('plan a coroutine by time', {'time': time})
        hours = time[0].split(':')
        try:
            sched.add_job(mail, 'cron', hour=int(hours[0]), minute=int(hours[1]), args=(bot, time[0]),
                          misfire_grace_time=120, id=time[0])
        except Exception:
            pass


async def cancel(old_time, new_time) -> None:
    global bot
    logging.info('Change time', {'old_time': old_time,
                                 'new_time': new_time})
    global sched
    try:
        sched.remove_job(old_time)
        sched.remove_job(new_time)
    except Exception:
        pass
    await scheduler(bot, [[new_time], [old_time]])


async def start_scheduler(_bot: Bot):
    global sched, bot
    if _bot is not None:
        bot = _bot
    logging.info('Configuring scheduler')
    sched = AsyncIOScheduler()
    times = await db.get_times()
    await scheduler(bot, times)
    sched.start()
