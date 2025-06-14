from functools import lru_cache
from uuid import UUID

import httpx
from loguru import logger

from app.api.schemas.answer import AnswerCreateSchema, AnswerDetailSchema
from app.api.schemas.interview import InterviewCreateSchema, InterviewDetailSchema
from app.api.schemas.user import (
    UserCreateResponseSchema,
    UserCreateSchema
)
from app.api.schemas.user_profile import UserProfileCreateSchema, \
    UserProfileSchema
from httpx_clients.interview_client.config import (
    InterviewAPISettings,
    get_interview_settings
)


class InterviewClient:
    def __init__(self, settings: InterviewAPISettings):
        self._base_url = settings.BASE_URL.rstrip("/")
        self._client = httpx.AsyncClient(
            base_url=self._base_url,
            timeout = 10.0
        )

    async def create_user(
            self, user_data: UserCreateSchema
    ) -> UserCreateResponseSchema:
        response = await self._client.post(
            "/users", json=user_data.model_dump()
        )
        response.raise_for_status()
        return UserCreateResponseSchema(**response.json())

    async def upload_cv(
            self,
            user_id: UUID,
            cv_file: bytes,
            filename: str
    ) -> UserProfileCreateSchema:
        files = {
            "cv_file": (filename, cv_file, "application/pdf")
        }
        data = {"user_id": str(user_id)}
        response = await self._client.post(
            "/user_profiles", data=data, files=files
        )
        response.raise_for_status()
        return response.json()

    async def create_interview(
            self,
            interview_data: InterviewCreateSchema
    ) -> InterviewDetailSchema:
        response = await self._client.post(
            "/interviews", json=interview_data.model_dump(mode="json")
        )
        response.raise_for_status()
        logger.info(f"🎤 Creating interview: {interview_data}")
        return InterviewDetailSchema(**response.json())

    async def get_user_profiles(self, user_id: UUID) -> list[UserProfileSchema]:
        user_id = {"user_id": str(user_id)}
        response = await self._client.get(
            "/user_profiles", params=user_id
        )
        response.raise_for_status()
        raw_data = response.json()
        return [UserProfileSchema(**item) for item in raw_data]


    async def get_interview(self, interview_id: UUID):
        response = await self._client.get(
            f"/interviews/{interview_id}"
        )
        response.raise_for_status()
        return InterviewDetailSchema(**response.json())

    async def answer_question(
            self,
            question_data: AnswerCreateSchema,
            interview_id: UUID
    ):
        response = await self._client.post(
            f"/interviews/{interview_id}/questions/answer",
            json=question_data.model_dump(mode="json")
        )
        response.raise_for_status()
        return AnswerDetailSchema(**response.json())


######################################################################

    async def close(self):
        await self._client.aclose()


@lru_cache
def get_client() -> InterviewClient:
    return InterviewClient(
        settings=get_interview_settings()
    )
