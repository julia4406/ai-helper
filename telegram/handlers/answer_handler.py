from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from loguru import logger

from app.api.schemas.answer import AnswerCreateSchema
from httpx_clients.interview_client.interview_client import get_client
from telegram.keyboards.main_menu import main_keyboard
from telegram.keyboards.question_menu import question_keyboard
from telegram.states.interview import InterviewStates

router = Router(name="answer")
client = get_client()


@router.callback_query(lambda c: c.data == "answer")
async def answer_question(
        callback: types.CallbackQuery,
        state: FSMContext
):
    """
    After pressing "Answer button" message from bot will appear
    User should enter answer into chat-window
    """
    await callback.message.answer(
        text="✏️ Please, enter your answer into chat window and sent in to me"
    )

    await state.set_state(InterviewStates.waiting_for_answer)


@router.message(InterviewStates.waiting_for_answer)
async def process_answer(
        message: types.Message,
        state: FSMContext
):
    """
    After typing answer into chat-window bot analyzes the answer,
    gives feedback on answer and send the next question
    """
    tg_data = await state.get_data()
    interview_id = tg_data.get("interview_id")
    question_id = tg_data.get("question_id")

    answer_text = message.text
    question_data = AnswerCreateSchema(text=answer_text, question_id=question_id)
    rated_answer = await client.answer_question(
        question_data,
        interview_id
    )

    await message.answer(
        text=f"Thanks for answer. I can score it in "
             f"{rated_answer.score}/5.0 points\n "
             f"My feedback: {rated_answer.feedback}"
    )

    await message.answer(
        text=f"Next question 😊 👇"
    )

    interview = await client.get_interview(interview_id)

    question = interview.questions[-1]
    await state.update_data(
        interview_id=interview.id,
        question_id=question.id
    )

    await message.answer(
        f"Question: {question.text}",
        reply_markup=question_keyboard()
    )


@router.callback_query(F.data == "finish_interview")
async def finish_interview(
        callback: types.CallbackQuery,
        state: FSMContext
):
    """
    Close current interview (in database) and
    return overall interview feedback
    """
    data = await state.get_data()
    user_id = data.get("user_id")
    profile_id = data.get("profile_id")
    interview_id = data.get("interview_id")
    logger.info("we have data: ", data)

    finished_interview_data = await client.finish_interview(
        interview_id=interview_id
    )
    feedback = finished_interview_data.feedback

    await callback.message.answer(
        text = f"Thank you. Here is short feedback on your interview.\n"
               f"{feedback}",
        reply_markup=main_keyboard()
    )

    # await state.clear()
    # await state.update_data(user_id=user_id, profile_id=profile_id)
