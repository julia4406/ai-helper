
from fastapi import APIRouter

from src.api.dependencies import InterviewServiceDep
from src.api.schemas.interview import InterviewCreateSchema


router = APIRouter(tags=["Interviews"], prefix="/interviews")

@router.post("", response_model=InterviewCreateSchema)
async def create_interview(
    interview_data: InterviewCreateSchema,
    interview_service: InterviewServiceDep
) -> InterviewCreateSchema:
    new_interview = await interview_service.create_interview(interview_data)
    return new_interview