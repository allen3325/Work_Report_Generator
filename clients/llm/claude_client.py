import os
from typing import Optional
import anthropic
from .base import LLMClient


class ClaudeClient(LLMClient):
    """
    Anthropic Claude LLM client implementation.

    Args:
        api_key (str): Anthropic API key
        model (str): Claude model name (required)
    """

    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model
        self.client = anthropic.Anthropic(api_key=api_key)

    def generate(self, prompt: str) -> str:
        """
        Generate text using Anthropic Claude API.

        Args:
            prompt (str): The input prompt for text generation

        Returns:
            str: Generated text

        Raises:
            Exception: If generation fails
        """
        try:
            response = self.client.messages.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1024*16,
            )

            return response.content[0].text.strip()
        except anthropic.AnthropicError as e:
            raise Exception(f"Claude API call failed: {str(e)}")

    def count_tokens(self, text: str) -> int:
        """
        Count tokens using Claude's tokenization.

        Args:
            text (str): Text to count tokens for

        Returns:
            int: Number of tokens
        """
        try:
            # Use Claude's token counting
            response = self.client.messages.count_tokens(
                model=self.model,
                messages=[{
                    "role": "user",
                    "content": text
                }],
            )
            return response.input_tokens
        except anthropic.AnthropicError as e:
            # Fallback to simple estimation if API call fails
            print(f"Warning: Claude token counting failed, using fallback: {str(e)}")
            return len(text.split())  # Simple word count as fallback

    def get_model_name(self) -> str:
        """
        Get the Claude model name.

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
        return "claude"
