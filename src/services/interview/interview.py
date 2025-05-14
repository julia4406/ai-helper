from uuid import UUID

from asyncpg import ForeignKeyViolationError
from loguru import logger

from src.api.schemas.interview import InterviewCreateSchema
from src.exceptions import ObjectNotFoundException
from src.repositories.interview import InterviewRepository
from src.repositories.user import UserRepository
from src.repositories.user_profile import ProfileRepository


class InterviewService:
    def __init__(
            self,
            interview_repo: InterviewRepository,
            user_repo: UserRepository,
            profile_repo: ProfileRepository
    ):
        self._interview_repo = interview_repo
        self._user_repo = user_repo
        self._profile_repo = profile_repo

    async def create_interview(self, data: InterviewCreateSchema):
        logger.info(f"Creating new interview with such data: {data}")

        user = await self._user_repo.get_user_by_id(user_id=data.user_id)

        if not user:
            logger.error(f"User not found")
            raise ObjectNotFoundException(data.user_id)

        if data.profile_id:
            # checks if profile exists then load data from existing profile
            user_profile = await self._profile_repo.get_user_profile_by_id(
                data.profile_id
            )
            data.load_from_user_profile(user_profile)

        new_interview = await self._interview_repo.create_interview(data=data)

        return new_interview
