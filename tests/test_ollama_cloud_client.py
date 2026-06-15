import pytest
from unittest.mock import patch, MagicMock
from clients.llm import create_llm_client
from clients.llm.ollama_cloud_client import OllamaCloudClient


def test_ollama_cloud_client_initialization():
    """Test that OllamaCloudClient initializes correctly with the right base URL."""
    client = OllamaCloudClient(
        api_key="ollama-test-key",
        model="llama3:cloud"
    )
    assert client.api_key == "ollama-test-key"
    assert client.model == "llama3:cloud"
    assert client.base_url == "https://ollama.com/v1"
    assert client.get_provider_name() == "ollama_cloud"
    assert client.get_model_name() == "llama3:cloud"


@patch("clients.llm.openai_compatible_client.openai.OpenAI")
def test_ollama_cloud_client_generate(mock_openai_class):
    """Test that OllamaCloudClient generate method functions using OpenAI completions."""
    mock_client_instance = MagicMock()
    mock_openai_class.return_value = mock_client_instance

    mock_chat = MagicMock()
    mock_client_instance.chat = mock_chat

    mock_completions = MagicMock()
    mock_chat.completions = mock_completions

    mock_response = MagicMock()
    mock_choice = MagicMock()
    mock_message = MagicMock()
    mock_message.content = "Ollama Cloud response text"
    mock_choice.message = mock_message
    mock_response.choices = [mock_choice]
    mock_completions.create.return_value = mock_response

    client = OllamaCloudClient(
        api_key="ollama-test-key",
        model="llama3:cloud"
    )

    result = client.generate("Hello Ollama Cloud")

    assert result == "Ollama Cloud response text"
    mock_openai_class.assert_called_once_with(api_key="ollama-test-key", base_url="https://ollama.com/v1")
    mock_completions.create.assert_called_once_with(
        model="llama3:cloud",
        messages=[{"role": "user", "content": "Hello Ollama Cloud"}]
    )


def test_factory_create_ollama_cloud():
    """Test that the create_llm_client factory supports ollama_cloud."""
    client = create_llm_client(
        provider="ollama_cloud",
        api_key="test-ollama-key",
        model="llama3:cloud"
    )
    assert isinstance(client, OllamaCloudClient)
    assert client.base_url == "https://ollama.com/v1"
    assert client.api_key == "test-ollama-key"
    assert client.model == "llama3:cloud"
