import asyncio
from datetime import datetime
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from tgBot.handlers import common

from config_reader import config
from logger import logger as log


async def main():
    bot = Bot(token=config.bot_token.get_secret_value())
    dp = Dispatcher(storage=MemoryStorage())
    dp["started_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    dp.include_routers(common.router)
    log.debug({"message": "start"})
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
