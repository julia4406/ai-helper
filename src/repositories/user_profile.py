from src.api.schemas.user_profile import UserProfileCreateSchema
from src.database.models.user_profile import UserProfile
from src.repositories.base import BaseRepository


class ProfileRepository(BaseRepository):
    model = UserProfile

    async def create_new_profile(
            self, profile_data: UserProfileCreateSchema
    ):
        # new_profile = await self.add(obj_data=profile_data.model_dump())
        # return new_profile.to_dto()
        pass
