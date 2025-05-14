from ctypes import c_voidp
from uuid import UUID

from src.api.schemas.user_profile import UserProfileCreateSchema, \
    UserProfileSchema
from src.clients.base import BaseLLMClient
from src.repositories.user_profile import ProfileRepository
from src.services.profile.prompts import PROFILE_CREATE_SYSTEM_PROMPT
from src.services.profile.tools import SaveUserProfile
from src.utils.pdf_reader import extract_text_from_pdf


class ProfileService:

    def __init__(
            self,
            llm_client: BaseLLMClient,
            profile_repo: ProfileRepository
    ):
        self._profile_repo = profile_repo
        self._llm_client = llm_client

    async def create_new_profile(self, profile_data:UserProfileCreateSchema):
        cv_content = await extract_text_from_pdf(profile_data.cv_file)

        # Передаємо контент CV LLMці для обробки
        # tools якось передаються

        text, tool_result = await self._llm_client.send_message(
            system_prompt=PROFILE_CREATE_SYSTEM_PROMPT,
            message=f"Here is user's CV text: {cv_content}\n"
                    f"Also, here is user's ID: {profile_data.user_id}\n",
            tools=[SaveUserProfile.to_function_definition()]
        )

        if tool_result:
            user_profile = await self._profile_repo.create_new_profile(
                profile_data=tool_result
            )

            return user_profile

        return RuntimeError("Failed to generate user profile")

    async def get_profiles(self, user_id: UUID) -> list[UserProfileSchema]:
        return await self._profile_repo.get_user_profiles(user_id)
