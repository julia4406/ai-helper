from aiogram import Router, types
from aiogram.filters import CommandStart

from httpx_clients.interview_client.interview_client import get_client
from telegram.handlers.start_handler import start_message

router = Router(name="start")
client = get_client()


@router.message(CommandStart())
async def start_handler(message: types.Message) -> None:

    telegram_id = str(message.from_user.id)
    text, reply_markup = await start_message(telegram_id)
    await message.answer(
            text,
            reply_markup=reply_markup
    )
