from aiogram.types import InlineKeyboardMarkup, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

from httpx_clients.interview_client.config import get_interview_settings

settings = get_interview_settings()


def interview_keyboard() -> InlineKeyboardMarkup:
    """Use in interview menu."""
    builder = InlineKeyboardBuilder()

    builder.button(
        text="📰 Get from my CV profile",
        callback_data="start_interview_from_cv" # викликати вибір профайла
    )
    builder.button(
        text="✒️ Manual setup",
        web_app=WebAppInfo(
            url=f"{settings.BASE_URL}/webapp/manual"
        )
    )

    builder.button(
        text="📲 Upload new CV",
        callback_data="upload_cv"
    )
    builder.button(
        text="↪️ Return",
        callback_data="return_to_start"
    )

    builder.adjust(2)

    return builder.as_markup()