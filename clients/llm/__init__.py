# LLM clients package initialization
from .base import LLMClient
from .openai_client import OpenAIClient
from .gemini_client import GeminiClient
from .claude_client import ClaudeClient


def create_llm_client(provider: str, api_key: str, model: str) -> LLMClient:
    """
    Create an LLM client based on the provider.

    Args:
        provider (str): LLM provider name (openai, gemini, claude)
        api_key (str): API key for the provider
        model (str): Model name for the provider

    Returns:
        LLMClient: Initialized LLM client

    Raises:
        ValueError: If provider is not supported
    """
    if provider == "openai":
        return OpenAIClient(api_key, model)
    elif provider == "gemini":
        return GeminiClient(api_key, model)
    elif provider == "claude":
        return ClaudeClient(api_key, model)
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")
