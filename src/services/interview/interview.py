import asyncio

from fastapi import HTTPException
from loguru import logger

from src.api.schemas.interview import InterviewCreateSchema
from src.api.schemas.question import QuestionCreateSchema
from src.clients.gemini.client import GeminiClient
from src.clients.prompts import QUESTION_GENERATION_SYSTEM_PROMPT
from src.exceptions import ObjectNotFoundException
from src.repositories.interview import InterviewRepository
from src.repositories.question import QuestionRepository
from src.repositories.user import UserRepository
from src.repositories.user_profile import ProfileRepository


class InterviewService:
    def __init__(
            self,
            interview_repo: InterviewRepository,
            user_repo: UserRepository,
            profile_repo: ProfileRepository,
            question_repo: QuestionRepository,
            llm_client: GeminiClient
    ):
        self._interview_repo = interview_repo
        self._user_repo = user_repo
        self._profile_repo = profile_repo
        self._question_repo = question_repo
        self._llm_client = llm_client

    async def create_interview(self, data: InterviewCreateSchema):
        logger.info(f"Creating new interview with such data: {data}")

        user = await self._user_repo.get_user_by_id(user_id=data.user_id)

        if not user:
            logger.error(f"User not found")
            raise ObjectNotFoundException("User", data.user_id)

        # checks if profile exists then load data from existing profile
        if data.profile_id:
            user_profile = await self._profile_repo.get_user_profile_by_id(
                data.profile_id
            )
            if not user_profile:
                raise ObjectNotFoundException("Profile", data.profile_id)

            data.load_from_user_profile(user_profile)

        try:
            new_interview = await self._interview_repo.create_interview(data=data)
            logger.info(f"Created new interview {new_interview}")

            question_text = await self.generate_question(data)

            await self._question_repo.create_question(
                question_data=QuestionCreateSchema(
                    text=question_text,
                    interview_id=new_interview.id
                )
            )

            # TODO gather couple of questions
            # question_tasks = []
            # for i in range(10):
            #     task = asyncio.create_task(
            #         self.generate_question(data)
            #     )
            #     question_tasks.append(task)
            #
            # questions = await asyncio.gather(*question_tasks)
            # logger.warning(f"{questions}")

            return new_interview

        except Exception as e:
            logger.error(f"Cannot create new interview.\n"
                         f"Error message:  {e}")
            raise HTTPException(status_code=400, detail=f"Error {e}")


    async def generate_question(self, data: InterviewCreateSchema):
        text, _ = await self._llm_client.send_message(
            system_prompt=self.question_prompt(data),
            message="Generate 1 question"
        )
        logger.info(f"Generated question: {text[:40]}")
        return text


    @staticmethod
    def question_prompt(data: InterviewCreateSchema):
        return QUESTION_GENERATION_SYSTEM_PROMPT.format(
            job_position=data.job_position,
            experience=data.experience,
            tech_stack=data.tech_stack
        )
