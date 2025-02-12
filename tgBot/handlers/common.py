
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message
import asyncio
from logger import logger as log

from api.services.service import Service
router = Router()
update_tasks = {}


@router.message(Command(commands=["start"]))
async def cmd_get(message: Message):
    await message.answer(
        text=(
            "Автоматизированный бот для арбитражной торговли между DEX ParaSwap и Jupiter. Он сравнивает цены на $LUNA в сетях BASE и SOLANA, выявляя возможности для получения прибыли."
            "\n\n"+"Используйте команду /push для получения обновлений."
            "\n\n"+"Используйте команду /get что бы запросить уведомление в любой момент."
        )
    )


@router.message(Command(commands=["get"]))
async def cmd_start(message: Message):
    await get_data(message, True)


async def process_paraswap_data(message: Message, check_spred: bool):
    print("________________________process_paraswap_data____________________________")
    data = await Service().calc_paraswap_amount()
    spread = float(data.spread)
    if spread > 1.5 or check_spred:
        msg = (
            f"<b>{abs(data.difference):.2f}$</b>"
            f" (<i>{spread:.2f}%</i>)"
            f" <b>{data.amount}</b>$"
            "\n"
            f"#LUNA SOL → BASE"
        )

        log.info({"message": msg,
                  "data": {
                      "logs": data.logs,
                      "amount": data.amount,
                      "usdc": data.amount,
                      "luna": data.luna,
                      "difference":  data.difference,
                      "spread": spread}}, label="paraswap")
        await message.answer(text=msg, parse_mode='HTML')
    print("____________________________________________________")


async def process_jupiter_data(message: Message, check_spred: bool):
    data = await Service().calc_jupiter_amount()
    spread = float(data.spread)
    if spread > 1.5 or check_spred:
        msg = (
            f"<b>{abs(data.difference):.2f}$</b>"
            f" (<i>{spread:.2f}%</i>)"
            f" <b>{data.amount}</b>$"
            "\n"
            f"#LUNA BASE → SOL"
        )
        log.info({"message": msg,
                  "data": {
                      "logs": data.logs,
                      "amount": data.amount,
                      "usdc": data.amount,
                      "luna": data.luna,
                      "difference":  data.difference,
                      "spread": spread}}, label="jupiter")
        await message.answer(text=msg, parse_mode='HTML')
    print("____________________________________________________")


async def get_data(message: Message, check_spred: bool = False):
    await asyncio.gather(
        process_paraswap_data(message, check_spred),
        process_jupiter_data(message, check_spred)
    )


async def send_updates(message: Message):
    while True:
        await get_data(message)
        await asyncio.sleep(5)


@router.message(Command(commands=["push"]))
async def cmd_push(message: Message):
    user_id = message.from_user.id
    if user_id not in update_tasks:
        update_tasks[user_id] = asyncio.create_task(send_updates(message))
        await message.answer("Обновления запущены. Используйте команду /stop для остановки.")
    else:
        await message.answer("Обновления уже запущены.")


@router.message(Command(commands=["stop"]))
async def cmd_stop(message: Message):
    user_id = message.from_user.id
    if user_id in update_tasks:
        update_tasks[user_id].cancel()
        del update_tasks[user_id]
        await message.answer("Обновления остановлены.")
    else:
        await message.answer("Обновления не запущены.")
