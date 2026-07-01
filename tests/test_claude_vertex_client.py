import pytest
from unittest.mock import patch, MagicMock
from clients.llm import create_llm_client
from clients.llm.claude_vertex_client import ClaudeVertexClient


def test_claude_vertex_client_initialization():
    """Test that ClaudeVertexClient initializes correctly."""
    with patch("clients.llm.claude_vertex_client.AnthropicVertex") as mock_vertex_class:
        client = ClaudeVertexClient(
            project_id="test-project",
            region="global",
            model="claude-sonnet-5"
        )
        assert client.project_id == "test-project"
        assert client.region == "global"
        assert client.model == "claude-sonnet-5"
        assert client.get_provider_name() == "claude_vertex"
        assert client.get_model_name() == "claude-sonnet-5"
        mock_vertex_class.assert_called_once_with(region="global", project_id="test-project")


def test_claude_vertex_client_generate():
    """Test that ClaudeVertexClient generate method functions correctly using AnthropicVertex messages API."""
    with patch("clients.llm.claude_vertex_client.AnthropicVertex") as mock_vertex_class:
        mock_client_instance = MagicMock()
        mock_vertex_class.return_value = mock_client_instance

        mock_messages = MagicMock()
        mock_client_instance.messages = mock_messages

        mock_response = MagicMock()
        mock_block = MagicMock()
        mock_block.type = "text"
        mock_block.text = "Hello! I am Claude Vertex."
        mock_response.content = [mock_block]
        mock_messages.create.return_value = mock_response

        client = ClaudeVertexClient(
            project_id="test-project",
            region="global",
            model="claude-sonnet-5"
        )

        result = client.generate("Hello Claude Vertex")

        assert result == "Hello! I am Claude Vertex."
        mock_messages.create.assert_called_once_with(
            model="claude-sonnet-5",
            messages=[{"role": "user", "content": "Hello Claude Vertex"}],
            thinking={"type": "adaptive"},
            output_config={"effort": "low"},
            max_tokens=1024 * 16,
        )


def test_claude_vertex_client_count_tokens():
    """Test that ClaudeVertexClient count_tokens method functions correctly."""
    with patch("clients.llm.claude_vertex_client.AnthropicVertex") as mock_vertex_class:
        mock_client_instance = MagicMock()
        mock_vertex_class.return_value = mock_client_instance

        mock_messages = MagicMock()
        mock_client_instance.messages = mock_messages

        mock_response = MagicMock()
        mock_response.input_tokens = 5
        mock_messages.count_tokens.return_value = mock_response

        client = ClaudeVertexClient(
            project_id="test-project",
            region="global",
            model="claude-sonnet-5"
        )

        # 1. Test when API method count_tokens is available and works
        tokens = client.count_tokens("Hello world")
        assert tokens == 5
        mock_messages.count_tokens.assert_called_once_with(
            model="claude-sonnet-5",
            messages=[{"role": "user", "content": "Hello world"}],
        )

        # 2. Test fallback when count_tokens fails
        mock_messages.count_tokens.side_effect = Exception("API Error")
        fallback_tokens = client.count_tokens("Hello world from unit test")
        assert fallback_tokens == 5  # 5 words in "Hello world from unit test"


def test_factory_create_claude_vertex():
    """Test that the create_llm_client factory supports claude_vertex."""
    with patch("clients.llm.claude_vertex_client.AnthropicVertex"):
        client = create_llm_client(
            provider="claude_vertex",
            project_id="test-project-factory",
            region="us-central1",
            model="claude-sonnet-5"
        )
        assert isinstance(client, ClaudeVertexClient)
        assert client.project_id == "test-project-factory"
        assert client.region == "us-central1"
        assert client.model == "claude-sonnet-5"
