from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup

from httpx_clients.interview_client.interview_client import get_client
from telegram.keyboards.main_menu import main_keyboard
from telegram.keyboards.start_menu import start_menu
from telegram.utils.dependencies_from_backend import provide_user_service

router = Router(name="start")
client = get_client()


async def start_message(telegram_id: str) -> tuple[str, InlineKeyboardMarkup]:
    user_service = await provide_user_service()

    try:
        await user_service.get_user_by_telegram_id(telegram_id)
        text = "👋 Welcome back! What do you want to do?"
        reply_markup=main_keyboard()

    except Exception as e:
        print("EXCEPTION IN start_message:", e)
        text = ("👋 Welcome! I'll help you to prepare to job-interview 😊 "
                "Please register to continue.")
        reply_markup=start_menu()

    return text, reply_markup
