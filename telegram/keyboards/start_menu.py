from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

from httpx_clients.interview_client.config import get_interview_settings

settings = get_interview_settings()


def start_menu() -> InlineKeyboardMarkup:
    """Use at start conversation with user."""
    builder = InlineKeyboardBuilder()

    print("WEBAPP URL:", f"{settings.BASE_URL}/webapp")
    print("TYPE:", type(f"{settings.BASE_URL}/webapp"))
    builder.button(
        text="📝 Register",
        web_app=WebAppInfo(
            url=f"{settings.BASE_URL}/webapp"
        )
    )

    return builder.as_markup()
