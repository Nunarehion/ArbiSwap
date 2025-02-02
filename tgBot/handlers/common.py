
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message

from api.services.service import Service
router = Router()


@router.message(Command(commands=["start"]))
async def cmd_start(message: Message):
    # data = Service().calc_amountCompare()
    await message.answer(
        text="work"
        # text=f"{data}",
    )
