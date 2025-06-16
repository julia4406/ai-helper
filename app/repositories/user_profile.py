from uuid import UUID

from sqlalchemy import select

from app.api.schemas.user_profile import UserProfileSchema
from app.database.models.user_profile import UserProfile
from app.repositories.base import BaseRepository


class ProfileRepository(BaseRepository):
    model = UserProfile

    async def create_new_profile(
            self, profile_data: UserProfileSchema
    ):
        new_profile = await self.add(obj_data=profile_data.model_dump(exclude={"id"}))
        return new_profile.to_dto()

    async def get_user_profiles(self, user_id: UUID):
        query = select(self.model).where(self.model.user_id == user_id)
        user_profiles = await self._session.scalars(query)
        return [profile.to_dto() for profile in user_profiles]

    async def get_user_profile_by_id(self, profile_id: UUID):
        return await self.get(profile_id)

