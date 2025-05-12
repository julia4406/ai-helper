from abc import ABC, abstractmethod


class BaseLLMClient(ABC):
    """
    base interface file for all LLM-clients when we want to use different LLMs
    """

    @abstractmethod
    async def send_message(self, system_prompt: str, message: str, tools: list):
        """
        can send message to LLM
        """
        pass
