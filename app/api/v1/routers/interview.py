from uuid import UUID

from fastapi import APIRouter

from app.api.dependencies import InterviewServiceDep, UserServiceDep
from app.api.schemas.answer import AnswerCreateSchema
from app.api.schemas.interview import InterviewCreateSchema, \
    InterviewFinishResponseSchema

router = APIRouter(tags=["Interviews"], prefix="/interviews")

@router.post("", response_model=InterviewCreateSchema)
async def create_interview(
    interview_data: InterviewCreateSchema,
    interview_service: InterviewServiceDep,
    user_service: UserServiceDep
) -> InterviewCreateSchema:
    if not interview_data.user_id and interview_data.telegram_id:
        user_id = await user_service.get_user_by_telegram_id(
            interview_data.telegram_id)
        interview_data.user_id = user_id
    new_interview = await interview_service.create_interview(interview_data)
    return new_interview


@router.get("/{interview_id}")
async def get_interview(
    interview_id: UUID,
    interview_service: InterviewServiceDep
):
    interview = await interview_service.get_interview_by_id(interview_id)

    return interview


@router.post("/{interview_id}/questions/answer")
async def answer_question(
    question_data: AnswerCreateSchema,
    interview_id: UUID,
    interview_service: InterviewServiceDep
):
    return await interview_service.create_answer_for_question(
        question_data, interview_id
    )


@router.post("/{interview_id}/finish", response_model=InterviewFinishResponseSchema)
async def finish_interview(
    interview_id: UUID,
    interview_service: InterviewServiceDep
):
    feedback = await interview_service.finish_interview(interview_id)

    return InterviewFinishResponseSchema(
        feedback=feedback,
        id=interview_id,
    )
