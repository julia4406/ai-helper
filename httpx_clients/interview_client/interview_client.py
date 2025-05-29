from functools import lru_cache
from uuid import UUID

import httpx

from app.api.schemas.interview import InterviewCreateSchema
from app.api.schemas.user import (
    UserCreateResponseSchema,
    UserCreateSchema
)
from app.api.schemas.user_profile import UserProfileCreateSchema
from httpx_clients.interview_client.config import (
    InterviewAPISettings,
    get_interview_settings
)


class InterviewClient:
    def __init__(self, settings: InterviewAPISettings):
        self._base_url = settings.BASE_URL.rstrip("/")
        self._client = httpx.AsyncClient(base_url=self._base_url)

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
    ) -> InterviewCreateSchema:
        response = await self._client.post(
            "/interviews", json=interview_data.model_dump()
        )
        response.raise_for_status()
        return InterviewCreateSchema(**response.json())


######################################################################

    async def close(self):
        await self._client.aclose()


@lru_cache
def get_client() -> InterviewClient:
    return InterviewClient(
        settings=get_interview_settings()
    )
