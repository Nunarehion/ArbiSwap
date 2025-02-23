import asyncio
from datetime import datetime
import logging
from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters.command import Command
from aiogram.fsm.storage.memory import MemoryStorage
from tgBot.handlers import common
from config_reader import config
from logger import logger as log
from api.services.service import Service
import sqlite3
import random as rd


def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY
        )
    ''')


def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cache (
            id INTEGER PRIMARY KEY,
            paraswap_message TEXT,
            jupiter_message TEXT
        )
    ''')

    conn.commit()
    conn.close()


init_db()


def add_user(user_id: int):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(
        'INSERT OR IGNORE INTO users (user_id) VALUES (?)', (user_id,))
    conn.commit()
    conn.close()


def remove_user(user_id: int):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM users WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()


def get_users():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT user_id FROM users')
    rows = cursor.fetchall()
    conn.close()
    return {row[0] for row in rows}


def add_cache_messages(paraswap_message: str, jupiter_message: str):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) FROM cache')
    count = cursor.fetchone()[0]

    if count == 0:
        cursor.execute('INSERT INTO cache (paraswap_message, jupiter_message) VALUES (?, ?)',
                       (paraswap_message, jupiter_message))
    else:
        cursor.execute('UPDATE cache SET paraswap_message = ?, jupiter_message = ?',
                       (paraswap_message, jupiter_message))

    conn.commit()
    conn.close()


def remove_cache_messages():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM cache')
    conn.commit()
    conn.close()


def get_paraswap_message():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT paraswap_message FROM cache')
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None


def get_jupiter_message():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT jupiter_message FROM cache')
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None


async def process_paraswap_data(bot, user_id, data, check_spred: bool):
    spread = float(data.spread)
    msg = (
        f"<b>{data.difference:.2f}$</b>"
        f" (<i>{spread:.2f}%</i>)"
        f" <b>{data.amount}</b>$"
        "\n"
        f"#LUNA BASE → SOL"
    )

    add_cache_messages(msg, get_jupiter_message())
    log.info(
        {
            "short": {
                "amount": data.amount,
                "usdc": data.usdc,
                "luna": data.luna,
                "difference": data.difference,
                "spread": spread
            },
            "logs": data.logs,
            "telegram": {
                "user_id": user_id,
                "message": msg
            }
        }, extra={'label': 'par', "file": "service/detail"}
    )

    if spread > 1.5 or check_spred:
        await bot.send_message(user_id, text=msg, parse_mode='HTML')
        await asyncio.sleep(1.3)


async def process_jupiter_data(bot, user_id, data, check_spred: bool):
    spread = float(data.spread)
    msg = (
        f"<b>{data.difference:.2f}$</b>"
        f" (<i>{spread:.2f}%</i>)"
        f" <b>{data.amount}</b>$"
        "\n"
        f"#LUNA SOL → BASE"
    )

    add_cache_messages(get_paraswap_message(), msg)
    log.info(
        {
            "short": {
                "amount": data.amount,
                "usdc": data.usdc,
                "luna": data.luna,
                "difference": data.difference,
                "spread": spread
            },
            "logs": data.logs,
            "telegram": {
                "user_id": user_id,
                "message": msg
            }
        }, extra={'label': 'jup', "file": "service/detail"}
    )

    if spread > 1.5 or check_spred:
        await bot.send_message(user_id, text=msg, parse_mode='HTML')
        await asyncio.sleep(1.7)


async def send_data(bot, check_spred: bool = False):
    user_ids = get_users()
    print("Current users:", user_ids)
    if user_ids:
        paraswap_data, jupiter_data = await asyncio.gather(
            Service().calc_paraswap_amount(),
            Service().calc_jupiter_amount()
        )
        for user_id in user_ids:
            await asyncio.gather(
                process_paraswap_data(
                    bot, user_id, paraswap_data, check_spred),
                process_jupiter_data(
                    bot, user_id, jupiter_data, check_spred)
            )


async def worker(bot, rpt):
    print(f"Daemon is running rpt for {rpt}ms")
    requestCount = 0
    errorsCount = 0
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    while True:
        log.debug({"requestCount": requestCount, "errorsCount": errorsCount, "rpt": rpt,
                   "start_time": start_time}, extra={"single_file": "info"})
        try:
            requestCount += 1
            await send_data(bot)
        except Exception as e:
            errorsCount += 1
            rpt *= 2
            log.error({"error": repr(e)})
        await asyncio.sleep(rpt + rd.uniform(0.1, 0.5))


async def main():
    bot = Bot(token=config.bot_token.get_secret_value())
    dp = Dispatcher(storage=MemoryStorage())
    dp["started_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    dp.include_routers(common.router)
    log.debug({"message": "start"})

    rpm = 60/9
    asyncio.create_task(worker(bot, rpm))
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
