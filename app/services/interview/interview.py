from uuid import UUID

from asyncpg import ForeignKeyViolationError
from fastapi import HTTPException
from loguru import logger

from app.api.schemas.answer import AnswerCreateSchema
from app.api.schemas.interview import (
    InterviewCreateSchema,
    InterviewDetailSchema
)
from app.api.schemas.question import QuestionCreateSchema
from app.clients.gemini.client import GeminiClient
from app.clients.prompts import (
    QUESTION_GENERATION_SYSTEM_PROMPT,
    ANSWER_RATING_PROMPT,
    INTERVIEW_RATING_PROMPT
)
from app.exceptions import ObjectNotFoundException
from app.repositories.answer import AnswerRepository
from app.repositories.interview import InterviewRepository
from app.repositories.question import QuestionRepository
from app.repositories.user import UserRepository
from app.repositories.user_profile import ProfileRepository
from app.services.interview.tool_definitions_interview import SaveAnswerRate


class InterviewService:
    def __init__(
            self,
            interview_repo: InterviewRepository,
            user_repo: UserRepository,
            profile_repo: ProfileRepository,
            question_repo: QuestionRepository,
            answer_repo: AnswerRepository,
            llm_client: GeminiClient
    ):
        self._interview_repo = interview_repo
        self._user_repo = user_repo
        self._profile_repo = profile_repo
        self._question_repo = question_repo
        self._answer_repo = answer_repo
        self._llm_client = llm_client

    async def create_interview(
            self, data: InterviewCreateSchema
    ) -> InterviewDetailSchema:
        logger.info(f"Start creating new interview with such data: {data}")

        user = await self._user_repo.get_user_by_id(user_id=data.user_id)

        if not user:
            logger.error(f"User not found")
            raise ObjectNotFoundException("User", data.user_id)

        if data.profile_id:
            user_profile = await self._profile_repo.get_user_profile_by_id(
                data.profile_id
            )
            if not user_profile:
                raise ObjectNotFoundException("Profile", data.profile_id)

            data.load_from_user_profile(user_profile)

        try:
            new_interview = await self._interview_repo.create_interview(data=data)
            logger.info(f"Finally: created new interview {new_interview}")

            question = await self.create_question(new_interview, is_first=True)
            full_interview = await self._interview_repo.get_interview_by_id(
                new_interview.id
            )

            return full_interview

        except ForeignKeyViolationError as e:
            logger.error(f"Cannot create new interview.\n"
                         f"Error message:  {e}")
            raise HTTPException(status_code=400, detail=f"Error {e}")

    async def finish_interview(self, interview_id: UUID) -> str:
        interview_info = await self.get_interview_by_id(interview_id)
        if not interview_info.is_active:
            raise HTTPException(
                status_code=400,
                detail=f"Interview with id {interview_id} is already finished"
            )
        feedback = await self.rate_interview(interview_info)
        await self._interview_repo.update(
            obj_id=interview_id,
            obj_new_data={
                "is_active": False,
                "feedback": feedback,
            }
        )

        return feedback

    async def create_question(
            self,
            data: InterviewCreateSchema | InterviewDetailSchema,
            is_first: bool = False
    ):
        question_text = await self._generate_question(data, is_first=is_first)
        logger.info(
            f"Generated question for interview {data.id}: {question_text}"
        )

        await self._question_repo.create_question(
            question_data=QuestionCreateSchema(
                text=question_text,
                interview_id=data.id
            )
        )

    async def get_interview_by_id(self, interview_id: UUID):
        interview = await self._interview_repo.get_interview_by_id(interview_id)

        if not interview:
            raise ObjectNotFoundException("Interview", interview_id)

        return interview

    async def create_answer_for_question(self, answer_data: AnswerCreateSchema,
                                         interview_id: UUID):
        await self._answer_repo.create_answer(answer_data=answer_data)
        interview_info = await self.get_interview_by_id(interview_id)
        rated_answer = await self.rate_answer(interview_info)
        await self.create_question(interview_info)

        return rated_answer

    async def rate_answer(self, interview_info: InterviewDetailSchema):
        _, answer_rate = await self._llm_client.send_message(
            system_prompt=ANSWER_RATING_PROMPT,
            message=f"{interview_info.model_dump()}"
                    f"You should rate the last answer and save result.",
            tools=[SaveAnswerRate.to_function_definition()]
        )
        logger.info(f"Rated answer: {answer_rate}")

        rated_answer = await self._answer_repo.update_answer(
            answer_id=answer_rate.pop("answer_id"),
            new_answer_data=answer_rate,
        )

        return rated_answer

    async def rate_interview(self, interview_info: InterviewDetailSchema):
        feedback, _ = await self._llm_client.send_message(
            system_prompt=INTERVIEW_RATING_PROMPT,
            message=f"{interview_info.model_dump()}"
                    f"You should rate the interview and return result",
        )
        logger.info(f"Rated interview: {feedback}")
        return feedback


    async def _generate_question(
            self,
            data: InterviewCreateSchema | InterviewDetailSchema,
            is_first: bool = False
    ):
        system_prompt = self.question_prompt(data=data)
        if is_first:
            system_prompt = self.first_question_prompt(data=data)

        text, _ = await self._llm_client.send_message(
            system_prompt=system_prompt,
            message="Generate 1 question"
        )
        logger.info(f"Generated question: {text[:40]}")
        return text

    @staticmethod
    def first_question_prompt(data: InterviewCreateSchema):
        return QUESTION_GENERATION_SYSTEM_PROMPT.format(
            job_position=data.job_position,
            experience=data.experience,
            tech_stack=data.tech_stack
        )

    @staticmethod
    def question_prompt(data: InterviewDetailSchema):
        return QUESTION_GENERATION_SYSTEM_PROMPT.format(
            job_position=data.job_position,
            experience=data.experience,
            tech_stack=data.tech_stack
        )
