from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from httpx_clients.interview_client.interview_client import get_client
from telegram.handlers.start_handler import start_message
from telegram.keyboards.main_menu import main_keyboard

router = Router(name="start")
client = get_client()


@router.message(CommandStart())
async def start_handler(message: types.Message, state: FSMContext) -> None:

    telegram_id = str(message.from_user.id)

    text, reply_markup = await start_message(telegram_id, state)
    await message.answer(
            text,
            reply_markup=reply_markup
    )


@router.callback_query(lambda c: c.data == "return_to_start")
async def return_to_start(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "👋 Welcome back! What do you want to do?",
        reply_markup=main_keyboard()
    )
