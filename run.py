import asyncio
import os
from dotenv import load_dotenv
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from tgBot.handlers import common

logging.basicConfig(level=logging.INFO)

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')

if not API_TOKEN:
    logging.error("API_TOKEN is not set. Please check your .env file.")
else:
    logging.info(f"API_TOKEN is set {API_TOKEN}")


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_routers(common.router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
