from aiogram import Router, types
from aiogram.filters import CommandStart

from telegram.keyboards.inline.menu import main_keyboard

router = Router(name="start")


@router.message(CommandStart())
async def start_handler(message: types.Message) -> None:

    await message.answer(
        "HELLO!",
        reply_markup=main_keyboard()
    )