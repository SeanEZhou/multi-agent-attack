from openai import OpenAI
import json
from typing import Optional, List, Dict, Any
from src.config import (
    AZUREAI_API_KEY,
    AZUREAI_BASE_URL,
    ORCHESTRATOR_MODEL,
    ORCHESTRATOR_TEMPERATURE
)


class AzureAIClient:
    """Wrapper for OpenAI-compatible API to be used by the orchestrator agent."""

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
        self.model = model or ORCHESTRATOR_MODEL
        self.temperature = temperature if temperature is not None else ORCHESTRATOR_TEMPERATURE

        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )

    def chat(
        self,
        messages: List[Dict[str, str]],
        tools: Optional[List[Dict[str, Any]]] = None,
        stream: bool = False
    ) -> Dict[str, Any]:
        """
        Send a chat request with optional tool definitions.

        Args:
            messages: List of message dicts with 'role' and 'content'
            tools: Optional list of tool definitions in OpenAI function calling format
            stream: Whether to stream the response

        Returns:
            Response dict with message and optional tool_calls
        """
        kwargs = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature,
            "max_tokens": 4096,
            "stream": stream
        }

        if tools:
            kwargs["tools"] = tools
            kwargs["tool_choice"] = "auto"

        response = self.client.chat.completions.create(**kwargs)

        # Transform to expected format
        message = response.choices[0].message

        result = {
            "message": {
                "role": message.role,
                "content": message.content or "",
                "tool_calls": None
            }
        }

        # Handle tool calls
        if hasattr(message, 'tool_calls') and message.tool_calls:
            result["message"]["tool_calls"] = [
                {
                    "id": tc.id,
                    "type": tc.type,
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments
                    }
                }
                for tc in message.tool_calls
            ]

        return result

    def generate(self, prompt: str, system: Optional[str] = None) -> str:
        """
        Generate text (simpler interface without chat history).

        Args:
            prompt: The user prompt
            system: Optional system prompt

        Returns:
            Generated text as a string
        """
        messages = []

        if system:
            messages.append({"role": "system", "content": system})

        messages.append({"role": "user", "content": prompt})

        result = self.chat(messages=messages)
        return result["message"]["content"]

    def is_available(self) -> bool:
        """
        Check if endpoint is available.

        Returns:
            True if server is available
        """
        try:
            # Try a simple request
            self.generate("test", system="reply with 'ok'")
            return True
        except Exception as e:
            print(f"Azure AI availability check failed: {e}")
            return False
