from uuid import UUID

from fastapi import APIRouter

from src.api.schemas.interview import InterviewCreateSchema

router = APIRouter(tags=["Interviews"], prefix="/interviews")

@router.post("")
async def create_interview(
    interview_data: InterviewCreateSchema,

):

    return {
        "content": "some message"
      }
