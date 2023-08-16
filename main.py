import asyncio
from aiogram import Bot, Dispatcher
from handlers.commands import register
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from data_manager.data_manager import start
from handlers.wearing import register_wearing
import os
from dotenv import load_dotenv
from modules.scheduler import start_scheduler


def register_handlers(dp):
    register(dp)
    register_wearing(dp)


async def main() -> None:
    global bot
    """
    Entry point
    """
    load_dotenv('.env')
    TOKEN_API = os.getenv('TOKEN_API')

    bot = Bot(TOKEN_API)
    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)
    start()
    register_handlers(dp)


    try:
        await dp.skip_updates()
        await start_scheduler(bot)
        await dp.start_polling()


    except Exception as _ex:
        print(_ex)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

