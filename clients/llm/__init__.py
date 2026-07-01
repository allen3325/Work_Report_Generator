# LLM clients package initialization
from typing import Optional
from .base import LLMClient
from .openai_client import OpenAIClient
from .gemini_client import GeminiClient
from .claude_client import ClaudeClient
from .openai_compatible_client import OpenAICompatibleClient
from .ollama_cloud_client import OllamaCloudClient
from .claude_vertex_client import ClaudeVertexClient


def create_llm_client(
    provider: str,
    api_key: Optional[str] = None,
    model: Optional[str] = None,
    base_url: Optional[str] = None,
    project_id: Optional[str] = None,
    region: Optional[str] = None,
) -> LLMClient:
    """
    Create an LLM client based on the provider.

    Args:
        provider (str): LLM provider name (openai, gemini, claude, claude_vertex, openai_compatible, ollama_cloud)
        api_key (Optional[str]): API key for the provider
        model (Optional[str]): Model name for the provider
        base_url (Optional[str]): Base URL for OpenAI-compatible client (e.g., vLLM)
        project_id (Optional[str]): Project ID for Claude Vertex AI
        region (Optional[str]): Region for Claude Vertex AI

    Returns:
        LLMClient: Initialized LLM client

    Raises:
        ValueError: If provider is not supported
    """
    if provider == "openai":
        if not api_key:
            raise ValueError("api_key is required for provider 'openai'")
        if not model:
            raise ValueError("model is required for provider 'openai'")
        return OpenAIClient(api_key, model)
    elif provider == "gemini":
        if not api_key:
            raise ValueError("api_key is required for provider 'gemini'")
        if not model:
            raise ValueError("model is required for provider 'gemini'")
        return GeminiClient(api_key, model)
    elif provider == "claude":
        if not api_key:
            raise ValueError("api_key is required for provider 'claude'")
        if not model:
            raise ValueError("model is required for provider 'claude'")
        return ClaudeClient(api_key, model)
    elif provider == "claude_vertex":
        if not project_id:
            import os
            project_id = os.getenv("CLAUDE_VERTEX_PROJECT_ID")
        if not project_id:
            raise ValueError("project_id or CLAUDE_VERTEX_PROJECT_ID environment variable is required for provider 'claude_vertex'")
        if not region:
            import os
            region = os.getenv("CLAUDE_VERTEX_REGION", "global")
        if not model:
            import os
            model = os.getenv("CLAUDE_VERTEX_MODEL")
        if not model:
            raise ValueError("model or CLAUDE_VERTEX_MODEL environment variable is required for provider 'claude_vertex'")
        return ClaudeVertexClient(project_id, region, model)
    elif provider == "openai_compatible":
        if not api_key:
            raise ValueError("api_key is required for provider 'openai_compatible'")
        if not model:
            raise ValueError("model is required for provider 'openai_compatible'")
        if not base_url:
            import os
            base_url = os.getenv("OPENAI_COMPATIBLE_BASE_URL")
        if not base_url:
            raise ValueError("base_url or OPENAI_COMPATIBLE_BASE_URL environment variable is required for provider 'openai_compatible'")
        return OpenAICompatibleClient(api_key, model, base_url)
    elif provider == "ollama_cloud":
        if not api_key:
            raise ValueError("api_key is required for provider 'ollama_cloud'")
        if not model:
            raise ValueError("model is required for provider 'ollama_cloud'")
        return OllamaCloudClient(api_key, model)
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")



