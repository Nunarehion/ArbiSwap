
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message
from logger import logger as log

from aiogram import types
from aiogram.fsm.context import FSMContext

from run import add_user, remove_user, get_users, get_paraswap_message, get_jupiter_message


router = Router()
# message.from_user.id


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
    paraswap_message = get_paraswap_message()
    jupiter_message = get_jupiter_message()

    if paraswap_message:
        await message.answer(paraswap_message, parse_mode='HTML')
    if jupiter_message:
        await message.answer(jupiter_message, parse_mode='HTML')

    if not paraswap_message and not jupiter_message:
        await message.answer("Нет кешированных сообщений.", parse_mode='HTML')


@router.message(Command(commands=["push"]))
async def cmd_push(message: types.Message):
    user_id = message.from_user.id
    if user_id not in get_users():
        add_user(user_id)
        await message.answer("Обновления запущены. Используйте команду /stop для остановки.")
    else:
        await message.answer("Обновления уже запущены.")


@router.message(Command(commands=["stop"]))
async def cmd_stop(message: types.Message):
    user_id = message.from_user.id
    if user_id in get_users():
        remove_user(user_id)
        await message.answer("Обновления остановлены.")
    else:
        await message.answer("Обновления не запущены.")
