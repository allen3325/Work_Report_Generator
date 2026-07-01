import os
from typing import Optional
from anthropic import AnthropicVertex
from .base import LLMClient


class ClaudeVertexClient(LLMClient):
    """
    Anthropic Claude on Google Cloud Vertex AI LLM client implementation.

    Args:
        project_id (str): Google Cloud Project ID
        region (str): Google Cloud Region (e.g., "us-central1", "global")
        model (str): Claude model name (required)
    """

    def __init__(self, project_id: str, region: str, model: str):
        self.project_id = project_id
        self.region = region
        self.model = model
        self.client = AnthropicVertex(region=region, project_id=project_id)

    def generate(self, prompt: str) -> str:
        """
        Generate text using Anthropic Vertex AI API.

        Args:
            prompt (str): The input prompt for text generation

        Returns:
            str: Generated text

        Raises:
            Exception: If generation fails
        """
        try:
            response = self.client.messages.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                thinking={"type": "adaptive"},
                output_config={"effort": "low"},
                max_tokens=1024 * 16,
            )

            text_blocks = [
                block.text for block in response.content if block.type == "text"
            ]
            return "".join(text_blocks).strip()
        except Exception as e:
            raise Exception(f"Claude Vertex API call failed: {str(e)}")

    def count_tokens(self, text: str) -> int:
        """
        Count tokens using Claude's tokenization.

        Args:
            text (str): Text to count tokens for

        Returns:
            int: Number of tokens
        """
        try:
            # Try to count tokens using the SDK's message count_tokens if available
            if hasattr(self.client.messages, "count_tokens"):
                response = self.client.messages.count_tokens(
                    model=self.model,
                    messages=[{
                        "role": "user",
                        "content": text
                    }],
                )
                return response.input_tokens
        except Exception as e:
            print(f"Warning: Claude Vertex token counting failed, using fallback: {str(e)}")
        
        # Fallback to simple estimation if API call or SDK support fails
        return len(text.split())

    def get_model_name(self) -> str:
        """
        Get the Claude Vertex model name.

        Returns:
            str: Model name
        """
        return self.model

    def get_provider_name(self) -> str:
        """
        Get the provider name.

        Returns:
            str: Provider name
        """
        return "claude_vertex"
