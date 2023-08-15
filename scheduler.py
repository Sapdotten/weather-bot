import asyncio

import aioschedule
import aioschedule as aios
from weather_parser import get_weather
from clothes import what_to_wear
import texts as tx
from aiogram import Bot
import data_manager.data_manager as bd


# @dp.message_handler()
# async def choose_your_dinner():
#     for user in set(the_users_without_dinner()):
#         await bot.send_message(chat_id = user, text = "Хей🖖 не забудь
#         выбрать свой ужин сегодня", reply_markup = menu_garnish)
#
# async def scheduler():
#     aioschedule.every().day.at("17:45").do(choose_your_dinner)
#     while True:
#         await aioschedule.run_pending()
#         await asyncio.sleep(1)
# async def on_startup(dp): 
#     asyncio.create_task(scheduler())
# 
# if __name__ == '__main__':
#     executor.start_polling(on_startup=on_startup)

async def mail_by_city(bot: Bot, ids: list[int], city_id: int, city_name: str) -> None:
    print('зфпустили рассылку на единый город')
    weather = await get_weather(city_id)
    text1 = tx.WEATHER_TODAY.substitute(city_name=city_name,
                                        max_t=weather['max_t'],
                                        min_t=weather['min_t'],
                                        descr=weather['descr'])
    text2 = await what_to_wear(weather['comfort'], weather['descr'])
    for id in ids:
        print('id получателя: ', id)
        await bot.send_message(chat_id=id[0], text=text1)
        await bot.send_message(chat_id=id[0], text=text2)


async def mail(bot: Bot, time: str) -> None:
    print('запустили рассылку на единое время')
    cities = await bd.get_cities_with_time(time)
    for city in cities:
        print(f'город: {city[0], city[1]}')
        users = await bd.get_users_with_time_city(time, city[0])
        await mail_by_city(bot, users, city[0], city[1])


async def scheduler(bot) -> None:
    print('запуск scheduler')
    times = await bd.get_times()
    for time in times:
        print('добавили корутину на время', time[0])
        aios.every().day.at(time[0]).do(mail, bot=bot, time=time[0])
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(bot: Bot):
    print('запуск онтсратпа')
    asyncio.create_task(scheduler(bot))
