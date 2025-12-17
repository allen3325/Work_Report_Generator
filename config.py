import argparse
import os
from typing import Dict, Any


def parse_arguments() -> argparse.Namespace:
    """
    Parse command line arguments for the report generator.

    Returns:
        argparse.Namespace: Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="Generate annual performance report from HackMD weekly notes"
    )

    # Required arguments
    parser.add_argument(
        "--start-date", type=str, required=True, help="Start date in format YYYY-MM-DD"
    )
    parser.add_argument(
        "--end-date", type=str, required=True, help="End date in format YYYY-MM-DD"
    )
    parser.add_argument(
        "--folder-name", type=str, required=True, help="Target folder name in HackMD"
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        required=True,
        help="Maximum token limit for the report",
    )
    parser.add_argument(
        "--llm-provider",
        type=str,
        required=True,
        choices=["openai", "gemini", "claude"],
        help="LLM service provider (openai, gemini, claude)",
    )
    parser.add_argument(
        "--year-tag", type=str, required=True, help="Year tag for HackMD tags"
    )

    return parser.parse_args()


def validate_env(llm_provider: str) -> None:
    """
    Validate environment variables based on the LLM provider.

    Args:
        llm_provider (str): The LLM provider to validate

    Raises:
        ValueError: If required environment variables are missing
    """
    # Check HackMD token
    if not os.getenv("HACKMD_API_TOKEN"):
        raise ValueError("Error: HACKMD_API_TOKEN is missing in environment variables")

    # Check LLM provider specific API key
    key_name = f"{llm_provider.upper()}_API_KEY"
    if not os.getenv(key_name):
        raise ValueError(f"Error: {key_name} is required for {llm_provider} provider")

    # Check LLM provider specific model
    model_name = f"{llm_provider.upper()}_MODEL"
    if not os.getenv(model_name):
        raise ValueError(f"Error: {model_name} is required for {llm_provider} provider")


def get_env_vars() -> Dict[str, Any]:
    """
    Get all relevant environment variables.

    Returns:
        Dict[str, Any]: Dictionary of environment variables
    """
    return {
        "HACKMD_API_TOKEN": os.getenv("HACKMD_API_TOKEN"),
        "HACKMD_API_URL": os.getenv("HACKMD_API_URL", "https://api.hackmd.io/v1"),
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
        "OPENAI_MODEL": os.getenv("OPENAI_MODEL"),
        "GEMINI_API_KEY": os.getenv("GEMINI_API_KEY"),
        "GEMINI_MODEL": os.getenv("GEMINI_MODEL"),
        "CLAUDE_API_KEY": os.getenv("CLAUDE_API_KEY"),
        "CLAUDE_MODEL": os.getenv("CLAUDE_MODEL"),
    }
