from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def main_keyboard() -> InlineKeyboardMarkup:
    """Use in main menu."""
    builder = InlineKeyboardBuilder()

    builder.button(
        text="📲 Upload CV",
        callback_data="upload_cv"
    )

    builder.button(
        text="🚀 Start interview",
        callback_data="interview"
    )

    builder.adjust(1)
    return builder.as_markup()
