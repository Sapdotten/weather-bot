import asyncio
import time
import logger
from aiogram import Bot
from aiogram import Dispatcher
import data.data_manager as db
from handlers.wearing import wearing_router
from modules.scheduler import start_scheduler
from handlers.commands import command_router
from aiogram.client.session.aiohttp import AiohttpSession
import config_manager


def register_routers(dp):
    dp.include_routers(command_router, wearing_router)


async def main() -> None:
    """
    Entry point
    """

    config_manager.start()
    logger.start()

    db.start()

    session = AiohttpSession()
    bot = Bot(config_manager.token(), session=session)
    dp = Dispatcher()
    register_routers(dp)
    try:
        await bot.delete_webhook()
        await start_scheduler(bot)
        await dp.start_polling(bot)
    except Exception as ex:
        print(ex)


print('Program starts')
if __name__ == '__main__':
    time.sleep(5)
    asyncio.run(main())
