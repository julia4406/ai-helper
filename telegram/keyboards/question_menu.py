from aiogram.types import InlineKeyboardMarkup, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

from httpx_clients.interview_client.config import get_interview_settings

settings = get_interview_settings()


def question_keyboard() -> InlineKeyboardMarkup:
    """Use in question menu."""
    builder = InlineKeyboardBuilder()

    builder.button(
        text="✏️ Answer",
        callback_data="answer"
    )
    builder.button(
        text="Finish interview",  # видає статистику
        callback_data="finish_interview"
    )
    builder.button(
        text="↪️ Return 🏠",  # поверне поки на головну
        callback_data="return_to_start"
    )

    builder.adjust(2)

    return builder.as_markup()