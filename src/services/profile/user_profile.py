from src.api.schemas.user_profile import UserProfileCreateSchema
from src.clients.base import BaseLLMClient
from src.repositories.user_profile import ProfileRepository
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
        pdf_content = await extract_text_from_pdf(profile_data.cv_file)

        # Передаємо контент CV LLMці для обробки
        llm_response = await self._llm_client.send_message(
            system_prompt="You are a helpful AI assistant that generates a user profile"
                          "based in the provided CV text. Your response should"
                          "contains job_position, experience in years, "
                          "tech_stack.",
            message=f"Here is user's CV text: {pdf_content}"
        )

        return llm_response


