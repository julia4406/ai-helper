from src.api.schemas.interview import InterviewCreateSchema
from src.repositories.interview import InterviewRepository


class InterviewService:
    def __init__(self, interview_repo: InterviewRepository):
        self._interview_repo = interview_repo

    async def create_interview(self, data: InterviewCreateSchema):
        return await self._interview_repo.create_interview(data=data)