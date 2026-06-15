import os
from typing import Optional
import openai
import tiktoken
from .base import LLMClient


class OpenAICompatibleClient(LLMClient):
    """
    OpenAI-compatible LLM client implementation.
    Suitable for connecting to endpoints like vLLM, Ollama, LiteLLM, etc.

    Args:
        api_key (str): API key for the provider (can be a dummy value for local endpoints)
        model (str): Model name for the provider
        base_url (str): Base URL of the OpenAI-compatible API
    """

    def __init__(self, api_key: str, model: str, base_url: str):
        self.api_key = api_key
        self.model = model
        self.base_url = base_url
        self.client = openai.OpenAI(api_key=api_key, base_url=base_url)

    def generate(self, prompt: str) -> str:
        """
        Generate text using OpenAI-compatible API.

        Args:
            prompt (str): The input prompt for text generation

        Returns:
            str: Generated text

        Raises:
            Exception: If generation fails
        """
        try:
            # We use standard chat completion endpoint as it is widely supported by
            # compatible backends like vLLM, Ollama, etc.
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            if response.choices and len(response.choices) > 0:
                content = response.choices[0].message.content
                return content.strip() if content else ""
            else:
                raise Exception("Empty response returned from OpenAI-compatible API")
        except openai.OpenAIError as e:
            raise Exception(f"OpenAI-compatible API call failed: {str(e)}")

    def count_tokens(self, text: str) -> int:
        """
        Count tokens using tiktoken.

        Args:
            text (str): Text to count tokens for

        Returns:
            int: Number of tokens
        """
        try:
            # Fallback to tiktoken for local/compatible models since they don't support online token counting API
            try:
                encoding = tiktoken.encoding_for_model(self.model)
            except KeyError:
                # Default encoding if the model is not registered in tiktoken
                encoding = tiktoken.get_encoding("cl100k_base")
            return len(encoding.encode(text))
        except Exception as e:
            print(f"Warning: Token counting failed, using fallback: {str(e)}")
            return len(text.split())  # Simple word count as fallback

    def get_model_name(self) -> str:
        """
        Get the model name.

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
        return "openai_compatible"
