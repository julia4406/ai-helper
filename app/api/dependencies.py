from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.clients.gemini.client import GeminiClientDep
from app.repositories.answer import AnswerRepository
from app.repositories.interview import InterviewRepository
from app.repositories.question import QuestionRepository
from app.repositories.user_profile import ProfileRepository
from app.services.interview.interview import InterviewService
from app.services.user import UserService
from app.repositories.user import UserRepository
from app.database.core.engine import get_async_session
from app.services.profile.user_profile import ProfileService

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

def get_profile_service(
        llm_client: GeminiClientDep,
        profile_repo: ProfileRepoDep
) -> ProfileService:
  return ProfileService(llm_client=llm_client, profile_repo=profile_repo)

ProfileServiceDep = Annotated[ProfileService, Depends(get_profile_service)]


def get_interview_repository(session: AsyncSessionDep) -> InterviewRepository:
  return InterviewRepository(session=session)

InterviewRepoDep = Annotated[InterviewRepository, Depends(get_interview_repository)]


def get_question_repository(session: AsyncSessionDep) -> QuestionRepository:
  return QuestionRepository(session=session)

QuestionRepoDep = Annotated[QuestionRepository, Depends(get_question_repository)]

def get_answer_repository(session: AsyncSessionDep) -> AnswerRepository:
  return AnswerRepository(session=session)

AnswerRepoDep = Annotated[AnswerRepository, Depends(get_answer_repository)]


def get_interview_service(
        interview_repo: InterviewRepoDep,
        user_repo: UserRepoDep,
        profile_repo: ProfileRepoDep,
        question_repo: QuestionRepoDep,
        answer_repo: AnswerRepoDep,
        llm_client: GeminiClientDep
) -> InterviewService:
  return InterviewService(
    interview_repo=interview_repo,
    user_repo=user_repo,
    profile_repo=profile_repo,
    question_repo=question_repo,
    answer_repo=answer_repo,
    llm_client=llm_client
  )

InterviewServiceDep = Annotated[InterviewService, Depends(get_interview_service)]
