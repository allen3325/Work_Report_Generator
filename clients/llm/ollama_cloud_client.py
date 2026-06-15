from .openai_compatible_client import OpenAICompatibleClient


class OllamaCloudClient(OpenAICompatibleClient):
    """
    Ollama Cloud LLM client implementation.

    Args:
        api_key (str): Ollama Cloud API key
        model (str): Ollama Cloud model name (required, e.g. "llama3:cloud")
    """

    def __init__(self, api_key: str, model: str):
        # Ollama Cloud API is OpenAI compatible and hosted at https://ollama.com/v1
        super().__init__(api_key=api_key, model=model, base_url="https://ollama.com/v1")

    def get_provider_name(self) -> str:
        """
        Get the provider name.

        Returns:
            str: Provider name
        """
        return "ollama_cloud"
