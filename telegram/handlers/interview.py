import json

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, \
    InlineKeyboardButton

from app.database.core.engine import async_session_maker
from app.repositories.user import UserRepository
from app.services.user import UserService
from httpx_clients.interview_client import interview_client
from httpx_clients.interview_client.interview_client import get_client
from telegram.keyboards.interview_menu import interview_keyboard
from telegram.keyboards.question_menu import question_keyboard

router = Router(name="interview")
client = get_client()

@router.callback_query(lambda c: c.data == "interview")
async def start_interview(callback: types.CallbackQuery):
    await callback.message.edit_text(
        text="⚙️ Setup interview data. I need couple parameters.",
        reply_markup=interview_keyboard()
    )
    await callback.answer()


@router.callback_query(lambda c: c.data == "start_interview_from_cv")
async def start_interview_from_cv(
        callback_query: CallbackQuery,
        state: FSMContext
):
    tg_data = await state.get_data()
    user_id = tg_data.get("user_id")

    user_profiles = await client.get_user_profiles(user_id)

    if not user_profiles:
        text = await callback_query.message.answer(
            "You don't have any uploaded CV yet."
        )
        reply_markup=interview_keyboard()
        return text, reply_markup

    buttons = []
    for profile in user_profiles:
        buttons.append(
            InlineKeyboardButton(
                text=profile.job_position,
                callback_data=f"select_cv: {profile.id}"
            )
        )
    profile_keyboard = InlineKeyboardMarkup(inline_keyboard=[buttons])
    await callback_query.message.answer(
        "Choose what profile you want to use:",
        reply_markup=profile_keyboard
    )


# Відповідь на натискання кнопки - має створюватись інтерв'ю і видаватись в бота
@router.callback_query(lambda c: c.data.startswith("select_cv:"))
async def handle_cv_selection(callback_query: CallbackQuery, state: FSMContext):
    profile_id = callback_query.data.split(":")[1]
    # TODO remove this message
    await callback_query.message.answer(f"✅ Обрано профіль ID: {profile_id}")


@router.callback_query(lambda c: c.data == "start_interview_manually")
async def start_interview_manually(callback: types.Message):
    pass


@router.message(F.web_app_data)
async def process_webapp_data(message: Message):
    try:
        data = json.loads(message.web_app_data.data)
    except Exception as e:
        await message.answer(f"Error in data handling: {e}")
        return

    interview_id = data.get("interview_id", "None")
    question = data.get("question", "Nema pytann`")

    await message.answer(
        f"🎯 Answer the question:\n👉 {question} in session of interview"
        f"with id {interview_id}",
        reply_markup=question_keyboard()
    )
