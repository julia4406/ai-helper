from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from httpx_clients.interview_client.config import get_interview_settings

settings = get_interview_settings()


def main_keyboard() -> InlineKeyboardMarkup:
    """Use in main menu."""
    builder = InlineKeyboardBuilder()

    builder.button(
        text="🧠 Upload CV",
        callback_data="upload_cv"
    )

    builder.button(
        text="🧑‍💻 Interview",
        callback_data="interview"
    )

    builder.adjust(1)
    return builder.as_markup()
