import asyncio
from aiogram import Bot
from aiogram.methods.delete_webhook import DeleteWebhook
from aiogram import Dispatcher
from handlers.commands import register_bot
from data_manager.data_manager import start
from handlers.wearing import wearing_router
import os
from dotenv import load_dotenv
from modules.scheduler import start_scheduler
from handlers.commands import command_router


def register_handlers(dp):
    dp.include_routers(command_router, wearing_router)


async def main() -> None:
    """
    Entry point
    """
    load_dotenv('.env')
    TOKEN_API = os.getenv('TOKEN_API')
    print('token_api is', TOKEN_API)

    bot = Bot(TOKEN_API)
    register_bot(bot)
    # storage = MemoryStorage()
    dp = Dispatcher()
    start()
    register_handlers(dp)
    await bot.delete_webhook()
    await start_scheduler(bot)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
