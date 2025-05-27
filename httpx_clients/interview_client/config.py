from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class InterviewAPISettings(BaseSettings):
    BASE_URL: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        env_prefix="INTERVIEW_"
    )


@lru_cache
def get_interview_settings() -> InterviewAPISettings:
    return InterviewAPISettings()
