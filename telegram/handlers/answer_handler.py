from aiogram import Router, types
from aiogram.fsm.context import FSMContext

from app.api.schemas.answer import AnswerCreateSchema
from httpx_clients.interview_client.interview_client import get_client
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
    answer_text = message.text
    tg_data = await state.get_data()
    interview_id = tg_data.get("interview_id")
    question_id = tg_data.get("question_id")

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
        text=f"Ok, next question 😊"
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
