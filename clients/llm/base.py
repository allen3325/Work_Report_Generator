from abc import ABC, abstractmethod
from typing import Optional


class LLMClient(ABC):
    """
    Abstract base class for LLM clients.

    All LLM clients should implement these methods to provide a consistent interface.
    """

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """
        Generate text based on the given prompt.

        Args:
            prompt (str): The input prompt for text generation

        Returns:
            str: Generated text

        Raises:
            Exception: If generation fails
        """
        pass

    @abstractmethod
    def count_tokens(self, text: str) -> int:
        """
        Count the number of tokens in the given text.

        Args:
            text (str): Text to count tokens for

        Returns:
            int: Number of tokens
        """
        pass

    @abstractmethod
    def get_model_name(self) -> str:
        """
        Get the name of the model being used.

        Returns:
            str: Model name
        """
        pass

    @abstractmethod
    def get_provider_name(self) -> str:
        """
        Get the name of the LLM provider.

        Returns:
            str: Provider name
        """
        pass
