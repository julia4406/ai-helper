from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.user_profile import ProfileRepository
from src.services.user import UserService
from src.repositories.user import UserRepository
from src.database.core.engine import get_async_session
from src.services.user_profile import ProfileService

AsyncSessionDep = Annotated[AsyncSession, Depends(get_async_session)]

def get_user_repository(session: AsyncSessionDep) -> UserRepository:
  return UserRepository(session=session)

UserRepoDep = Annotated[UserRepository, Depends(get_user_repository)]

def get_user_service(user_repo: UserRepoDep) -> UserService:
  return UserService(user_repo=user_repo)

UserServiceDep = Annotated[UserService, Depends(get_user_service)]


def get_profile_repository(session: AsyncSessionDep) -> ProfileRepository:
  return ProfileRepository(session=session)

ProfileRepoDep = Annotated[ProfileRepository, Depends(get_profile_repository)]

def get_profile_service(profile_repo: ProfileRepoDep) -> ProfileService:
  return ProfileService(profile_repo=profile_repo)

ProfileServiceDep = Annotated[ProfileService, Depends(get_profile_service)]
