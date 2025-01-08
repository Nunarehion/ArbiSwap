from aiogram import F, Router
from aiogram.filters import Command

from aiogram.types import Message

router = Router()

@router.message(Command(commands=["start"]))
async def cmd_start(message: Message):
    await message.answer(
        text="Выберите, что хотите заказать: "
             "блюда (/food) или напитки (/drinks).",
    )

from api.exchanges.jupiter import RealClient, pprint  