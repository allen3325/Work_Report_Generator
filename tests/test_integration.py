import pytest
import os
import sys
from unittest.mock import patch, MagicMock

sys.path.insert(0, "/home/os-chewei.chang/Projects/report_generator")
from main import main
from config import parse_arguments


def test_main_workflow_mock():
    """Test the main workflow with mocked components."""

    # Mock environment variables
    test_env = {
        "HACKMD_API_TOKEN": "test_token",
        "OPENAI_API_KEY": "test_openai_key",
        "OPENAI_MODEL": "gpt-4",
        "HACKMD_API_URL": "https://api.hackmd.io/v1",
    }

    # Mock command line arguments
    test_args = [
        "--start-date",
        "2024-01-01",
        "--end-date",
        "2024-01-31",
        "--folder-name",
        "Test Folder",
        "--max-tokens",
        "10000",
        "--llm-provider",
        "openai",
        "--year-tag",
        "2024",
    ]

    with (
        patch.dict(os.environ, test_env, clear=True),
        patch("sys.argv", ["main.py"] + test_args),
        patch("main.HackMDClient") as mock_hackmd,
        patch("main.create_llm_client") as mock_llm_factory,
        patch("main.save_local_report") as mock_save_local,
        patch("builtins.print") as mock_print,
    ):

        # Setup mocks
        mock_hackmd_instance = MagicMock()
        mock_hackmd.return_value = mock_hackmd_instance

        mock_llm_instance = MagicMock()
        mock_llm_instance.get_provider_name.return_value = "openai"
        mock_llm_instance.get_model_name.return_value = "gpt-4"
        mock_llm_instance.count_tokens.return_value = 100
        mock_llm_instance.generate.return_value = "# Test Report Content"
        mock_llm_factory.return_value = mock_llm_instance

        mock_save_local.return_value = "test_report.md"
        mock_hackmd_instance.upload_note.return_value = "https://hackmd.io/test"

        # Mock note data
        mock_note = {
            "id": "test_note_id",
            "title": "Test Note",
            "createdAt": 1704067200000,  # 2024-01-01
            "folderPaths": [{"name": "Test Folder"}],
            "content": "Test content",
        }

        mock_hackmd_instance.get_notes.return_value = [mock_note]
        mock_hackmd_instance.filter_notes_by_folder_and_date.return_value = [mock_note]
        mock_hackmd_instance.get_note_content.return_value = mock_note

        # Run main function
        try:
            main()
        except SystemExit:
            pass  # Expected for test

        # Verify calls
        mock_hackmd.assert_called_once()
        mock_llm_factory.assert_called_once_with(provider="openai", api_key="test_openai_key", model="gpt-4")
        mock_hackmd_instance.get_notes.assert_called_once()
        mock_hackmd_instance.filter_notes_by_folder_and_date.assert_called_once()
        mock_hackmd_instance.get_note_content.assert_called_once_with("test_note_id")
        mock_llm_instance.count_tokens.assert_called_once()
        mock_llm_instance.generate.assert_called_once()
        mock_save_local.assert_called_once()
        mock_hackmd_instance.upload_note.assert_called_once()

        # Verify print calls (success messages)
        print_calls = [str(call) for call in mock_print.call_args_list]
        success_messages = [
            "Starting report generation",
            "Clients initialized",
            "Fetching notes from HackMD",
            "Filtering notes",
            "Retrieving full content",
            "Building prompt",
            "Generating report",
            "Saving report locally",
            "Uploading to HackMD",
            "Report generation completed",
        ]

        for msg in success_messages:
            assert any(
                msg in str(call) for call in mock_print.call_args_list
            ), f"Expected print message containing '{msg}'"


def test_main_workflow_token_limit_exceeded():
    """Test the main workflow when token limit is exceeded."""

    # Mock environment variables
    test_env = {
        "HACKMD_API_TOKEN": "test_token",
        "OPENAI_API_KEY": "test_openai_key",
        "OPENAI_MODEL": "gpt-4",
        "HACKMD_API_URL": "https://api.hackmd.io/v1",
    }

    # Mock command line arguments
    test_args = [
        "--start-date",
        "2024-01-01",
        "--end-date",
        "2024-01-31",
        "--folder-name",
        "Test Folder",
        "--max-tokens",
        "50",  # Low limit
        "--llm-provider",
        "openai",
        "--year-tag",
        "2024",
    ]

    with (
        patch.dict(os.environ, test_env, clear=True),
        patch("sys.argv", ["main.py"] + test_args),
        patch("main.HackMDClient") as mock_hackmd,
        patch("main.create_llm_client") as mock_llm_factory,
        patch("builtins.print") as mock_print,
    ):

        # Setup mocks
        mock_hackmd_instance = MagicMock()
        mock_hackmd.return_value = mock_hackmd_instance

        mock_llm_instance = MagicMock()
        mock_llm_instance.count_tokens.return_value = 100  # Exceeds limit of 50
        mock_llm_factory.return_value = mock_llm_instance

        # Mock note data
        mock_note = {
            "id": "test_note_id",
            "title": "Test Note",
            "createdAt": 1704067200000,
            "folderPaths": [{"name": "Test Folder"}],
            "content": "Test content",
        }

        mock_hackmd_instance.get_notes.return_value = [mock_note]
        mock_hackmd_instance.filter_notes_by_folder_and_date.return_value = [mock_note]
        mock_hackmd_instance.get_note_content.return_value = mock_note

        # Run main function and expect SystemExit due to token limit
        with pytest.raises(SystemExit):
            main()

        # Verify error message
        error_calls = [
            str(call) for call in mock_print.call_args_list if "Error" in str(call)
        ]
        assert any(
            "Total token count" in call and "exceeds limit" in call
            for call in error_calls
        ), "Expected token limit exceeded error message"
