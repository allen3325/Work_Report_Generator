# LLM clients package initialization
from typing import Optional
from .base import LLMClient
from .openai_client import OpenAIClient
from .gemini_client import GeminiClient
from .claude_client import ClaudeClient
from .openai_compatible_client import OpenAICompatibleClient
from .ollama_cloud_client import OllamaCloudClient


def create_llm_client(provider: str, api_key: str, model: str, base_url: Optional[str] = None) -> LLMClient:
    """
    Create an LLM client based on the provider.

    Args:
        provider (str): LLM provider name (openai, gemini, claude, openai_compatible, ollama_cloud)
        api_key (str): API key for the provider
        model (str): Model name for the provider
        base_url (Optional[str]): Base URL for OpenAI-compatible client (e.g., vLLM)

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
    elif provider == "openai_compatible":
        if not base_url:
            import os
            base_url = os.getenv("OPENAI_COMPATIBLE_BASE_URL")
        if not base_url:
            raise ValueError("base_url or OPENAI_COMPATIBLE_BASE_URL environment variable is required for provider 'openai_compatible'")
        return OpenAICompatibleClient(api_key, model, base_url)
    elif provider == "ollama_cloud":
        return OllamaCloudClient(api_key, model)
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")


