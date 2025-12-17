import pytest
import os
import sys
from unittest.mock import patch

sys.path.insert(0, "/home/os-chewei.chang/Projects/report_generator")
from config import parse_arguments, validate_env, get_env_vars


def test_parse_arguments():
    """Test argument parsing with valid inputs."""
    test_args = [
        "--start-date",
        "2024-01-01",
        "--end-date",
        "2024-12-31",
        "--folder-name",
        "Test Folder",
        "--max-tokens",
        "100000",
        "--llm-provider",
        "openai",
        "--year-tag",
        "2024",
    ]

    with patch("sys.argv", ["generate_report.py"] + test_args):
        args = parse_arguments()

        assert args.start_date == "2024-01-01"
        assert args.end_date == "2024-12-31"
        assert args.folder_name == "Test Folder"
        assert args.max_tokens == 100000
        assert args.llm_provider == "openai"
        assert args.year_tag == "2024"


def test_parse_arguments_missing_required():
    """Test argument parsing with missing required arguments."""
    test_args = ["--start-date", "2024-01-01", "--folder-name", "Test Folder"]

    with patch("sys.argv", ["generate_report.py"] + test_args):
        with pytest.raises(SystemExit):
            parse_arguments()


def test_parse_arguments_invalid_provider():
    """Test argument parsing with invalid LLM provider."""
    test_args = [
        "--start-date",
        "2024-01-01",
        "--end-date",
        "2024-12-31",
        "--folder-name",
        "Test Folder",
        "--max-tokens",
        "100000",
        "--llm-provider",
        "invalid_provider",
        "--year-tag",
        "2024",
    ]

    with patch("sys.argv", ["generate_report.py"] + test_args):
        with pytest.raises(SystemExit):
            parse_arguments()


def test_validate_env_missing_hackmd_token():
    """Test environment validation with missing HackMD token."""
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(ValueError, match="HACKMD_API_TOKEN is missing"):
            validate_env("openai")


def test_validate_env_missing_llm_key():
    """Test environment validation with missing LLM API key."""
    with patch.dict(os.environ, {"HACKMD_API_TOKEN": "test_token"}, clear=True):
        with pytest.raises(ValueError, match="OPENAI_API_KEY is required"):
            validate_env("openai")


def test_validate_env_missing_llm_model():
    """Test environment validation with missing LLM model."""
    with patch.dict(
        os.environ,
        {"HACKMD_API_TOKEN": "test_token", "OPENAI_API_KEY": "test_openai_key"},
        clear=True,
    ):
        with pytest.raises(ValueError, match="OPENAI_MODEL is required"):
            validate_env("openai")


def test_validate_env_valid():
    """Test environment validation with all required variables."""
    with patch.dict(
        os.environ,
        {
            "HACKMD_API_TOKEN": "test_token",
            "OPENAI_API_KEY": "test_openai_key",
            "OPENAI_MODEL": "gpt-4",
        },
        clear=True,
    ):
        # Should not raise any exception
        validate_env("openai")


def test_get_env_vars():
    """Test getting environment variables."""
    with patch.dict(
        os.environ,
        {
            "HACKMD_API_TOKEN": "test_token",
            "HACKMD_API_URL": "https://test.api.hackmd.io/v1",
            "OPENAI_API_KEY": "test_openai_key",
            "OPENAI_MODEL": "gpt-4",
            "GEMINI_API_KEY": "test_gemini_key",
            "GEMINI_MODEL": "gemini-2.5-flash",
            "CLAUDE_API_KEY": "test_claude_key",
            "CLAUDE_MODEL": "claude-sonnet-4-5",
        },
        clear=True,
    ):
        env_vars = get_env_vars()

        assert env_vars["HACKMD_API_TOKEN"] == "test_token"
        assert env_vars["HACKMD_API_URL"] == "https://test.api.hackmd.io/v1"
        assert env_vars["OPENAI_API_KEY"] == "test_openai_key"
        assert env_vars["OPENAI_MODEL"] == "gpt-4"
        assert env_vars["GEMINI_API_KEY"] == "test_gemini_key"
        assert env_vars["GEMINI_MODEL"] == "gemini-2.5-flash"
        assert env_vars["CLAUDE_API_KEY"] == "test_claude_key"
        assert env_vars["CLAUDE_MODEL"] == "claude-sonnet-4-5"


def test_get_env_vars_default_url():
    """Test getting environment variables with default HackMD URL."""
    with patch.dict(
        os.environ,
        {
            "HACKMD_API_TOKEN": "test_token",
            "OPENAI_API_KEY": "test_openai_key",
            "OPENAI_MODEL": "gpt-4",
        },
        clear=True,
    ):
        env_vars = get_env_vars()

        assert env_vars["HACKMD_API_URL"] == "https://api.hackmd.io/v1"
