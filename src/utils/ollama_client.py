import requests
import json
from typing import Optional, List, Dict, Any
from src.config import OLLAMA_BASE_URL, OLLAMA_MODEL, ORCHESTRATOR_TEMPERATURE


class OllamaClient:
    """Wrapper for Ollama API to be used by the orchestrator agent."""

    def __init__(
        self,
        base_url: Optional[str] = None,
        model: Optional[str] = None,
        temperature: Optional[float] = None
    ):
        self.base_url = base_url or OLLAMA_BASE_URL
        self.model = model or OLLAMA_MODEL
        self.temperature = temperature if temperature is not None else ORCHESTRATOR_TEMPERATURE

    def chat(
        self,
        messages: List[Dict[str, str]],
        tools: Optional[List[Dict[str, Any]]] = None,
        stream: bool = False
    ) -> Dict[str, Any]:
        """
        Send a chat request to Ollama with optional tool definitions.

        Args:
            messages: List of message dicts with 'role' and 'content'
            tools: Optional list of tool definitions in OpenAI function calling format
            stream: Whether to stream the response

        Returns:
            Response dict with message and optional tool_calls
        """
        url = f"{self.base_url}/api/chat"

        payload = {
            "model": self.model,
            "messages": messages,
            "stream": stream,
            "options": {
                "temperature": self.temperature
            }
        }

        if tools:
            payload["tools"] = tools

        response = requests.post(url, json=payload)

        # Better error handling
        if response.status_code != 200:
            print(f"Error response from Ollama: {response.text}")
            print(f"Payload sent: {json.dumps(payload, indent=2)}")
        response.raise_for_status()

        result_data = response.json()

        # Convert Ollama response to our expected format
        message = result_data.get("message", {})

        result = {
            "message": {
                "role": message.get("role", "assistant"),
                "content": message.get("content", ""),
                "tool_calls": None
            }
        }

        # Handle tool calls if present
        if "tool_calls" in message and message["tool_calls"]:
            # Store tool calls in Ollama's native format (arguments as object, not string)
            # This is important for multi-turn conversations
            result["message"]["tool_calls"] = message["tool_calls"]

        return result

    def generate(self, prompt: str, system: Optional[str] = None) -> str:
        """
        Generate text using Ollama API (simpler interface without chat history).

        Args:
            prompt: The user prompt
            system: Optional system prompt

        Returns:
            Generated text as a string
        """
        url = f"{self.base_url}/api/generate"

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": self.temperature
            }
        }

        if system:
            payload["system"] = system

        response = requests.post(url, json=payload)
        response.raise_for_status()

        return response.json()["response"]

    def is_available(self) -> bool:
        """
        Check if Ollama server is available and the model is pulled.

        Returns:
            True if server is available and model exists
        """
        try:
            # Check if server is running
            response = requests.get(f"{self.base_url}/api/tags")
            response.raise_for_status()

            # Check if the model is available
            models = response.json().get("models", [])
            model_names = [m["name"] for m in models]

            return any(self.model in name for name in model_names)
        except Exception as e:
            print(f"Ollama availability check failed: {e}")
            return False
