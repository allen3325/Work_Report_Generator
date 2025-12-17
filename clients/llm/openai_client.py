import os
from typing import Optional
import openai
from .base import LLMClient


class OpenAIClient(LLMClient):
    """
    OpenAI LLM client implementation.

    Args:
        api_key (str): OpenAI API key
        model (str): OpenAI model name (required)
    """

    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model
        self.client = openai.OpenAI(api_key=api_key)

    def generate(self, prompt: str) -> str:
        """
        Generate text using OpenAI API.

        Args:
            prompt (str): The input prompt for text generation

        Returns:
            str: Generated text

        Raises:
            Exception: If generation fails
        """
        try:
            response = self.client.responses.create(
                model=self.model,
                input=prompt,
            )

            return response.output[0].content[0].text.strip()
        except openai.OpenAIError as e:
            raise Exception(f"OpenAI API call failed: {str(e)}")

    def count_tokens(self, text: str) -> int:
        """
        Count tokens using OpenAI's tokenization.

        Args:
            text (str): Text to count tokens for

        Returns:
            int: Number of tokens
        """
        try:
            # Use OpenAI's token counting
            response = self.client.responses.input_tokens.count(
                model=self.model,
                input=text,
            )
            return response.input_tokens
        except openai.OpenAIError as e:
            # Fallback to simple estimation if API call fails
            print(f"Warning: OpenAI token counting failed, using fallback: {str(e)}")
            return len(text.split())  # Simple word count as fallback

    def get_model_name(self) -> str:
        """
        Get the OpenAI model name.

        Returns:
            str: Model name
        """
        return self.model

    def get_provider_name(self) -> str:
        """
        Get the provider name.

        Returns:
            str: Provider name
        """
        return "openai"
