import httpx

from app.api.schemas.user import UserCreateResponseSchema, UserCreateSchema
from httpx_clients.interview_client.config import InterviewAPISettings


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

    async def close(self):
        await self._client.aclose()
