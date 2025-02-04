
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message

import asyncio

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


async def get_data(message: Message, check_spred: bool = False):
    data = Service().calc_amountCompare()
    print(float(abs(data.paraswap_USDC-data.amount)/data.amount*100))
    if float(abs(data.paraswap_USDC-data.amount)/data.amount*100) > 1.5 or check_spred:
        print(
            f"{abs(data.paraswap_USDC-data.amount):.2f}$ ({abs(data.paraswap_USDC-data.amount)/data.amount*100:.2f}%) {data.amount}$"
            "\n"
            f"#LUNA SOL → BASE"
        )
        await message.answer(
            text=(
                f"{abs(data.paraswap_USDC-data.amount):.2f}$ ({abs(data.paraswap_USDC-data.amount)/data.amount*100:.2f}%) {data.amount}$"
                "\n"
                f"#LUNA SOL → BASE"
            ),
        )
    print(float(abs(data.jupiter_USDC-data.amount)/data.amount*100))
    if float(abs(data.jupiter_USDC-data.amount)/data.amount*100) > 1.5 or check_spred:
        print(f"{abs(data.jupiter_USDC-data.amount):.2f}$ ({abs(data.jupiter_USDC-data.amount)/data.amount*100:.2f}%) {data.amount}$"
              "\n"
              f"#LUNA BASE → SOL")
        await message.answer(
            text=(
                f"{abs(data.jupiter_USDC-data.amount):.2f}$ ({abs(data.jupiter_USDC-data.amount)/data.amount*100:.2f}%) {data.amount}$"
                "\n"
                f"#LUNA BASE → SOL"
            ),
        )


async def send_updates(message: Message):
    while True:
        await get_data(message)
        await asyncio.sleep(10)


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
