from typing import Annotated

from fastapi import Depends
from google import genai
from google.genai import types
from loguru import logger

from src.clients.base import BaseLLMClient
from src.clients.gemini.config import get_gemini_settings


class GeminiClient(BaseLLMClient):
    def __init__(self):
        self._settings = get_gemini_settings()

    async def send_message(
            self,
            system_prompt: str,
            message: str
    ):
        client = genai.Client(api_key=self._settings.API_KEY)
        logger.debug(f"Sending message to Gemini: {message}")

        response = client.models.generate_content(
            model=self._settings.MODEL,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt),
            contents=message
        )

        return response.text


def get_gemini_client() -> BaseLLMClient:
    return GeminiClient()


GeminiClientDep = Annotated[GeminiClient, Depends(get_gemini_client)]
