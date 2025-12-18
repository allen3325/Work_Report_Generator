import os
from typing import Optional
from google import genai
from google.genai import types
from .base import LLMClient


class GeminiClient(LLMClient):
    """
    Google Gemini LLM client implementation.

    Args:
        api_key (str): Google Gemini API key
        model (str): Gemini model name (required)
    """

    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model
        self.client = genai.Client(api_key=api_key)

    def generate(self, prompt: str) -> str:
        """
        Generate text using Google Gemini API.

        Args:
            prompt (str): The input prompt for text generation

        Returns:
            str: Generated text

        Raises:
            Exception: If generation fails
        """
        try:
            generate_content_config = types.GenerateContentConfig(
                thinking_config=types.ThinkingConfig(
                    thinking_level="HIGH",
                ),
            )

            response = self.client.models.generate_content(
                model=self.model,
                config=generate_content_config,
                contents=prompt
            )

            return response.text if response.text else ""
        except Exception as e:
            raise Exception(f"Gemini API call failed: {str(e)}")

    def count_tokens(self, text: str) -> int:
        """
        Count tokens using Gemini's tokenization.

        Args:
            text (str): Text to count tokens for

        Returns:
            int: Number of tokens
        """
        try:
            # Use Gemini's token counting
            token_count = self.client.models.count_tokens(
                model=self.model,
                contents=text
            )
            return token_count.total_tokens if token_count.total_tokens else 0
        except Exception as e:
            # Fallback to simple estimation if API call fails
            print(f"Warning: Gemini token counting failed, using fallback: {str(e)}")
            return len(text.split())  # Simple word count as fallback

    def get_model_name(self) -> str:
        """
        Get the Gemini model name.

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
        return "gemini"
