from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

from httpx_clients.interview_client.config import get_interview_settings

settings = get_interview_settings()


def main_keyboard() -> InlineKeyboardMarkup:
    """Use in main menu."""
    builder = InlineKeyboardBuilder()
    builder.button(
        text="LogIn",
        callback_data="start"
    )
    builder.button(
        text="📝 Register",
        web_app=WebAppInfo(
            url=f"{settings.BASE_URL}/webapp"
        )
    )

    return builder.as_markup()
