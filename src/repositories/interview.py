from src.api.schemas.interview import InterviewCreateSchema
from src.database.models import Interview
from src.repositories.base import BaseRepository


class InterviewRepository(BaseRepository):
    model = Interview

    async def create_interview(self,data: InterviewCreateSchema):
        new_interview = await self.add(
            obj_data=data.model_dump(exclude={"user_profile_id"})
        )
        return new_interview.to_dto()