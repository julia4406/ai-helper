from aiogram import Router, types
from aiogram.filters import CommandStart

from httpx_clients.interview_client.interview_client import get_client
from telegram.keyboards.main_menu import main_keyboard
from telegram.keyboards.start_menu import start_menu
from telegram.utils.dependencies_from_backend import provide_user_service

router = Router(name="start")
client = get_client()

# TODO add functionality for login user and add telegram_id to db
@router.message(CommandStart())
async def start_handler(message: types.Message) -> None:

    telegram_id = str(message.from_user.id)
    user_service = await provide_user_service()

    try:
        await user_service.get_user_by_telegram_id(telegram_id)
        await message.answer(
            "👋 Welcome back! What do you want to do?",
            reply_markup=main_keyboard()
        )
    except Exception:
        await message.answer(
            "👋 Welcome! I'll help you to prepare to job-interview 😊 "
            "Please register to continue.",
            reply_markup=start_menu()
        )
