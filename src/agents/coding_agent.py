from typing import Optional
from src.utils.openai_client import OpenAIClient
from src.core.models import CodeResult


class CodingAgent:
    """
    Coding agent that generates code based on subtask descriptions.
    Acts as a 'tool' that the orchestrator can call.
    Uses OpenAI API (GPT-3.5/4) for code generation.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        temperature: Optional[float] = None
    ):
        self.client = OpenAIClient(api_key=api_key, model=model, temperature=temperature)

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

        # Extract filename if mentioned in the code (simple heuristic)
        filename = self._extract_filename(generated_code, language)

        return CodeResult(
            subtask_id=subtask_id,
            code=generated_code,
            language=language,
            filename=filename
        )

    def _extract_filename(self, code: str, language: Optional[str]) -> Optional[str]:
        """
        Try to extract a filename from the generated code.
        This is a simple heuristic - looks for common patterns like:
        - # filename: example.py
        - // filename: example.js
        """
        lines = code.split('\n')
        for line in lines[:5]:  # Check first 5 lines
            line_lower = line.lower().strip()
            if 'filename:' in line_lower:
                # Extract filename after "filename:"
                filename = line_lower.split('filename:')[1].strip()
                # Remove comment markers
                filename = filename.replace('#', '').replace('//', '').strip()
                return filename

        # If no filename found, return None
        return None

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
