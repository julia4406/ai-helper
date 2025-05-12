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
        self.llm_client = llm_client

    async def create_new_profile(self, profile_data:UserProfileCreateSchema):
        pdf_content = await extract_text_from_pdf(profile_data.cv_file)

        # Треба передавати тепер контент нашого резюме ЛЛМці
        ...


