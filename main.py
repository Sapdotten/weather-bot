import asyncio
from aiogram import Bot, Dispatcher
from handlers.commands import register
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from data_manager.data_manager import start
from handlers.wearing import register_wearing
from modules.scheduler import on_startup
import os
from dotenv import load_dotenv


def register_handlers(dp):
    register(dp)
    register_wearing(dp)


async def main() -> None:
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
    # on_startup_with_args = partial(on_startup, bot=bot)

    try:
        await dp.skip_updates()
        await on_startup(bot)
        await dp.start_polling()

    except Exception as _ex:
        print(_ex)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
