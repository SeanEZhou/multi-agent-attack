from typing import Optional
from src.utils.openai_client import OpenAIClient
from src.core.models import CodeResult


class CodingAgent:
    """
    Coding agent that generates code based on subtask descriptions.
    Acts as a 'tool' that the orchestrator can call.
    Uses Azure OpenAI API for code generation.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: Optional[str] = None,
        temperature: Optional[float] = None
    ):
        self.client = OpenAIClient(
            api_key=api_key,
            base_url=base_url,
            model=model,
            temperature=temperature
        )

    def generate_code(
        self,
        subtask_id: int,
        description: str,
        context: Optional[str] = None,
        language: Optional[str] = None
    ) -> CodeResult:
        """
        Generate code for a given subtask.

        Args:
            subtask_id: ID of the subtask
            description: Description of what code to generate
            context: Optional context or requirements
            language: Optional target programming language

        Returns:
            CodeResult containing the generated code
        """
        system_prompt = (
            "You are an expert coding assistant. Generate clean, well-documented code "
            "based on the given description. Include comments where helpful. "
            "Provide ONLY the code without additional explanations unless asked."
        )

        # Build the user prompt
        prompt_parts = [f"Generate code for the following task:\n\n{description}"]

        if context:
            prompt_parts.append(f"\nContext:\n{context}")

        if language:
            prompt_parts.append(f"\nTarget language: {language}")

        prompt = "\n".join(prompt_parts)

        # Generate code using OpenAI
        generated_code = self.client.generate_code(prompt, system_prompt)

        return CodeResult(
            subtask_id=subtask_id,
            code=generated_code,
            language=language,
            filename=None
        )

    def get_tool_definition(self) -> dict:
        """
        Return the tool definition for this agent in OpenAI function calling format.
        This allows the orchestrator to call this agent as a tool.
        """
        return {
            "type": "function",
            "function": {
                "name": "generate_code",
                "description": (
                    "Generate code for a specific subtask. This is a powerful coding assistant "
                    "that can create clean, well-documented code based on descriptions. "
                    "Use this tool when you need to delegate code generation for a subtask."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "subtask_id": {
                            "type": "integer",
                            "description": "Unique identifier for this subtask"
                        },
                        "description": {
                            "type": "string",
                            "description": "Clear description of what code to generate"
                        },
                        "context": {
                            "type": "string",
                            "description": "Optional additional context or requirements for the code"
                        },
                        "language": {
                            "type": "string",
                            "description": "Target programming language (e.g., 'python', 'javascript', 'java')"
                        }
                    },
                    "required": ["subtask_id", "description"]
                }
            }
        }
