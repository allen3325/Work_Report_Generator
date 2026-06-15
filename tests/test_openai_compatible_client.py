import pytest
from unittest.mock import patch, MagicMock
import openai
from clients.llm import create_llm_client
from clients.llm.openai_compatible_client import OpenAICompatibleClient


def test_openai_compatible_client_initialization():
    """Test that OpenAICompatibleClient initializes correctly."""
    client = OpenAICompatibleClient(
        api_key="test-api-key",
        model="test-model",
        base_url="http://localhost:8000/v1"
    )
    assert client.api_key == "test-api-key"
    assert client.model == "test-model"
    assert client.base_url == "http://localhost:8000/v1"
    assert client.get_provider_name() == "openai_compatible"
    assert client.get_model_name() == "test-model"


@patch("clients.llm.openai_compatible_client.openai.OpenAI")
def test_openai_compatible_client_generate(mock_openai_class):
    """Test the generate method of OpenAICompatibleClient."""
    # Setup mock
    mock_client_instance = MagicMock()
    mock_openai_class.return_value = mock_client_instance

    mock_chat = MagicMock()
    mock_client_instance.chat = mock_chat

    mock_completions = MagicMock()
    mock_chat.completions = mock_completions

    mock_response = MagicMock()
    mock_choice = MagicMock()
    mock_message = MagicMock()
    mock_message.content = "Generated text content"
    mock_choice.message = mock_message
    mock_response.choices = [mock_choice]
    mock_completions.create.return_value = mock_response

    # Initialize client
    client = OpenAICompatibleClient(
        api_key="test-key",
        model="gpt-3.5-turbo",
        base_url="http://localhost:8000/v1"
    )

    # Call generate
    result = client.generate("Hello, world!")

    # Assert results
    assert result == "Generated text content"
    mock_completions.create.assert_called_once_with(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello, world!"}]
    )


@patch("clients.llm.openai_compatible_client.openai.OpenAI")
def test_openai_compatible_client_generate_failure(mock_openai_class):
    """Test that generate propagates errors correctly."""
    # Setup mock to raise API error
    mock_client_instance = MagicMock()
    mock_openai_class.return_value = mock_client_instance
    mock_client_instance.chat.completions.create.side_effect = openai.APIError(
        message="API Error",
        request=MagicMock(),
        body=None
    )

    client = OpenAICompatibleClient(
        api_key="test-key",
        model="gpt-3.5-turbo",
        base_url="http://localhost:8000/v1"
    )

    with pytest.raises(Exception) as exc_info:
        client.generate("Hello, world!")

    assert "OpenAI-compatible API call failed" in str(exc_info.value)


@patch("clients.llm.openai_compatible_client.openai.OpenAI")
def test_openai_compatible_client_generate_empty_response(mock_openai_class):
    """Test that generate raises error on empty response choices."""
    mock_client_instance = MagicMock()
    mock_openai_class.return_value = mock_client_instance
    mock_client_instance.chat.completions.create.return_value = MagicMock(choices=[])

    client = OpenAICompatibleClient(
        api_key="test-key",
        model="gpt-3.5-turbo",
        base_url="http://localhost:8000/v1"
    )

    with pytest.raises(Exception) as exc_info:
        client.generate("Hello, world!")

    assert "Empty response returned" in str(exc_info.value)


@patch("clients.llm.openai_compatible_client.openai.OpenAI")
def test_openai_compatible_client_count_tokens(mock_openai_class):
    """Test token counting for OpenAICompatibleClient using tiktoken."""
    client = OpenAICompatibleClient(
        api_key="test-key",
        model="gpt-3.5-turbo",
        base_url="http://localhost:8000/v1"
    )

    # gpt-3.5-turbo is a known model in tiktoken
    tokens = client.count_tokens("Hello world")
    assert tokens > 0


@patch("clients.llm.openai_compatible_client.openai.OpenAI")
@patch("clients.llm.openai_compatible_client.tiktoken.encoding_for_model")
def test_openai_compatible_client_count_tokens_fallback(mock_encoding, mock_openai_class):
    """Test token counting fallback behavior when tiktoken raises error."""
    mock_encoding.side_effect = KeyError("Model not found")

    client = OpenAICompatibleClient(
        api_key="test-key",
        model="some-unknown-model",
        base_url="http://localhost:8000/v1"
    )

    # Should fall back to cl100k_base which is a valid encoding in tiktoken
    tokens = client.count_tokens("Hello world from an unknown model!")
    assert tokens > 0


@patch("clients.llm.openai_compatible_client.openai.OpenAI")
@patch("clients.llm.openai_compatible_client.tiktoken.get_encoding")
@patch("clients.llm.openai_compatible_client.tiktoken.encoding_for_model")
def test_openai_compatible_client_count_tokens_all_fail_fallback(mock_encoding_for_model, mock_get_encoding, mock_openai_class):
    """Test token counting fallback to word count when all tiktoken calls fail."""
    mock_encoding_for_model.side_effect = Exception("System error")
    mock_get_encoding.side_effect = Exception("System error")

    client = OpenAICompatibleClient(
        api_key="test-key",
        model="gpt-3.5-turbo",
        base_url="http://localhost:8000/v1"
    )

    # Should fall back to word split count: 4 words -> 4 tokens
    tokens = client.count_tokens("Hello world test string")
    assert tokens == 4


def test_factory_create_openai_compatible():
    """Test that the create_llm_client factory supports openai_compatible."""
    with patch.dict("os.environ", {"OPENAI_COMPATIBLE_BASE_URL": "http://localhost:8000/v1"}):
        client = create_llm_client(
            provider="openai_compatible",
            api_key="test-key",
            model="test-model"
        )
        assert isinstance(client, OpenAICompatibleClient)
        assert client.base_url == "http://localhost:8000/v1"
        assert client.api_key == "test-key"
        assert client.model == "test-model"


def test_factory_create_openai_compatible_with_explicit_url():
    """Test factory with explicit base_url passed as keyword argument."""
    client = create_llm_client(
        provider="openai_compatible",
        api_key="test-key",
        model="test-model",
        base_url="http://explicit-url:8000/v1"
    )
    assert isinstance(client, OpenAICompatibleClient)
    assert client.base_url == "http://explicit-url:8000/v1"
