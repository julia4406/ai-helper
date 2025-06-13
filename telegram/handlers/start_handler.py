from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup

from app.database.core.engine import async_session_maker
from app.repositories.user import UserRepository
from app.services.user import UserService
from httpx_clients.interview_client.interview_client import get_client
from telegram.keyboards.main_menu import main_keyboard
from telegram.keyboards.start_menu import start_menu

router = Router(name="start")
client = get_client()


async def start_message(
        telegram_id: str, state: FSMContext
) -> tuple[str, InlineKeyboardMarkup]:
    async with async_session_maker() as session:
        user_service = UserService(UserRepository(session=session))

        try:
            user_id = await user_service.get_user_by_telegram_id(telegram_id)
            await state.clear()

            await state.update_data(user_id=user_id)
            text = "👋 Welcome back! What do you want to do?"
            reply_markup=main_keyboard()

        except Exception as e:
            print("EXCEPTION IN start_message:", e)
            text = ("👋 Welcome! I'll help you to prepare to job-interview 😊 "
                    "Please register to continue.")
            reply_markup=start_menu()

        return text, reply_markup
