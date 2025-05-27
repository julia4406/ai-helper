from aiogram import Router, types
from aiogram.filters import CommandStart

from telegram.keyboards.inline.menu import main_keyboard

router = Router(name="start")

# TODO add functionality for login user and add telegram_id to db
@router.message(CommandStart())
async def start_handler(message: types.Message) -> None:

    await message.answer(
        "Hello! I'll help you to prepare to job-interview 😊",
        reply_markup=main_keyboard()
    )
