from aiogram import Router, types

from telegram.keyboards.interview_menu import interview_keyboard

router = Router(name="interview")


@router.callback_query(lambda c: c.data == "interview")
async def start_interview(callback: types.CallbackQuery):
    await callback.message.edit_text(
        text="⚙️ Setup interview data. I need couple parameters.",
        reply_markup=interview_keyboard()
    )
    await callback.answer()


@router.callback_query(lambda c: c.data == "start_interview_from_cv")
async def start_interview_from_cv(callback: types.CallbackQuery):
    pass


@router.callback_query(lambda c: c.data == "start_interview_manually")
async def start_interview_manually(callback: types.CallbackQuery):
    pass

