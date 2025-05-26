from uuid import UUID

from app.api.schemas.user_profile import UserProfileCreateSchema, \
    UserProfileSchema
from app.clients.gemini.client import GeminiClient
from app.exceptions import ObjectNotFoundException
from app.repositories.user_profile import ProfileRepository
from app.clients.prompts import PROFILE_CREATE_SYSTEM_PROMPT
from app.services.profile.tool_definitions_user_profile import SaveUserProfile
from app.utils.pdf_reader import extract_text_from_pdf


class ProfileService:

    def __init__(
            self,
            llm_client: GeminiClient,
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

    async def get_user_profile_by_id(self, profile_id: UUID):
        profile = await self._profile_repo.get_user_profile_by_id(profile_id)
        if not profile:
            raise ObjectNotFoundException("Profile", profile_id)
        return profile
