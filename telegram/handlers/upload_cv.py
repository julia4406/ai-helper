import json

import httpx
from aiogram import Router, types

from app.database.core.engine import async_session_maker
from app.exceptions import ObjectNotFoundException
from app.repositories.user import UserRepository
from app.services.user import UserService
from httpx_clients.interview_client.interview_client import get_client
from telegram.keyboards.main_menu import main_keyboard


router = Router(name="upload_cv")
client = get_client()

@router.callback_query(lambda c: c.data == "upload_cv")
async def start_upload_cv(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer("📎 Send pdf-file with your CV")


@router.message(lambda message: message.document is not None)
async def handle_upload_cv(message: types.Message):
    telegram_id = str(message.from_user.id)
    async with async_session_maker() as session:
        user_service = UserService(UserRepository(session=session))
        try:
            user_id = await user_service.get_user_by_telegram_id(telegram_id)

            document = message.document
            file = await message.bot.get_file(document.file_id)
            file_path = file.file_path
            file_bytes = await message.bot.download_file(file_path)

            result = await client.upload_cv(
                user_id=user_id,
                cv_file=file_bytes.read(),
                filename=document.file_name
            )
            await message.answer("✅ CV uploaded!", reply_markup=main_keyboard())

        except ObjectNotFoundException as e:
            await message.answer(
                "❌ User didn't found. Register!",
                reply_markup=main_keyboard()
            )

        except httpx.HTTPStatusError as e:
            try:
                error_detail = e.response.json().get("detail", "Unknown error")
            except  (json.JSONDecodeError, ValueError, TypeError):
                error_detail = e.response.text

            await message.answer(
                "⚠️ Sorry, we couldn't process your CV.\n\n"
                f"❌ {str(error_detail)}\n\n"
                "📄 Please upload a valid CV file in PDF format that contains "
                "information about your work experience, skills, and job history.",
                reply_markup=main_keyboard()
            )
