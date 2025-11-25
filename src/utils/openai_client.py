from openai import OpenAI
from typing import Optional
from src.config import (
    AZUREAI_API_KEY,
    AZUREAI_BASE_URL,
    CODING_AGENT_MODEL,
    CODING_AGENT_TEMPERATURE
)


class OpenAIClient:
    """Wrapper for OpenAI-compatible API to be used by the coding agent."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: Optional[str] = None,
        temperature: Optional[float] = None
    ):
        self.api_key = api_key or AZUREAI_API_KEY
        # Use OpenAI v1 compatible endpoint
        base = base_url or AZUREAI_BASE_URL
        self.base_url = f"{base}openai/v1" if not base.endswith('/v1') else base
        self.model = model or CODING_AGENT_MODEL
        self.temperature = temperature if temperature is not None else CODING_AGENT_TEMPERATURE

        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )

    def generate_code(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """
        Generate code using OpenAI-compatible API.

        Args:
            prompt: The user prompt describing what code to generate
            system_prompt: Optional system prompt to guide the model

        Returns:
            Generated code as a string
        """
        messages = []

        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        messages.append({"role": "user", "content": prompt})

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
        )

        return response.choices[0].message.content

    def chat(self, messages: list) -> str:
        """
        Send a list of messages to OpenAI-compatible API.

        Args:
            messages: List of message dicts with 'role' and 'content'

        Returns:
            Response content as a string
        """
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
        )

        return response.choices[0].message.content
