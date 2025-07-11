from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class TelegramSettings(BaseSettings):
    TOKEN: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        env_prefix="TELEGRAM_"
    )


@lru_cache
def get_tg_settings() -> TelegramSettings:
    return TelegramSettings()
