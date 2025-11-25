import json
from typing import Optional, List, Dict, Any
from src.utils.azure_ai_client import AzureAIClient
from src.agents.coding_agent import CodingAgent
from src.core.models import Task, SubTask, CodeResult, FinalResult
from src.config import MAX_ORCHESTRATOR_ITERATIONS


class OrchestratorAgent:
    """
    Orchestrator agent that breaks down tasks and delegates to the coding agent.
    Uses Azure AI Studio for planning and coordination.
    Treats the coding agent as a 'tool' that can be called multiple times.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_iterations: Optional[int] = None
    ):
        self.client = AzureAIClient(
            api_key=api_key,
            base_url=base_url,
            model=model,
            temperature=temperature
        )
        self.coding_agent = CodingAgent()
        self.max_iterations = max_iterations or MAX_ORCHESTRATOR_ITERATIONS

        # Store conversation history
        self.messages: List[Dict[str, Any]] = []

        # Store subtasks and results
        self.subtasks: List[SubTask] = []
        self.code_results: List[CodeResult] = []

    def process_task(self, task: Task, verbose: bool = True) -> FinalResult:
        """
        Process a task by breaking it down and delegating to the coding agent.

        Args:
            task: The main task to process
            verbose: Whether to print progress information

        Returns:
            FinalResult with assembled code and summary
        """
        if verbose:
            print(f"\n{'='*80}")
            print(f"ORCHESTRATOR: Processing task")
            print(f"{'='*80}")
            print(f"Task: {task.description}\n")

        # Initialize the conversation with system prompt and task
        system_prompt = self._create_system_prompt()
        user_prompt = self._create_initial_prompt(task)

        self.messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        # Get tool definition from coding agent
        tools = [self.coding_agent.get_tool_definition()]

        # Iterative loop: orchestrator plans and calls tools until satisfied
        for iteration in range(self.max_iterations):
            if verbose:
                print(f"\n--- Iteration {iteration + 1} ---")

            # Get response from Ollama with tool calling
            response = self.client.chat(messages=self.messages, tools=tools)

            assistant_message = response.get("message", {})
            self.messages.append(assistant_message)

            # Check if there are tool calls
            tool_calls = assistant_message.get("tool_calls")

            if tool_calls:
                if verbose:
                    print(f"Orchestrator is calling {len(tool_calls)} tool(s)...")

                # Execute each tool call
                for tool_call in tool_calls:
                    tool_name = tool_call.get("function", {}).get("name")
                    tool_args = tool_call.get("function", {}).get("arguments", {})

                    if isinstance(tool_args, str):
                        tool_args = json.loads(tool_args)

                    if verbose:
                        print(f"\nTool call: {tool_name}")
                        print(f"Arguments: {json.dumps(tool_args, indent=2)}")

                    # Execute the tool (coding agent)
                    if tool_name == "generate_code":
                        result = self._execute_coding_agent(tool_args, verbose)

                        # Add tool result to conversation
                        tool_response = {
                            "role": "tool",
                            "content": json.dumps({
                                "subtask_id": result.subtask_id,
                                "code": result.code,
                                "filename": result.filename,
                                "language": result.language
                            })
                        }
                        self.messages.append(tool_response)

            else:
                # No tool calls - orchestrator is done
                if verbose:
                    print("\nOrchestrator has finished planning and delegation.")

                final_message = assistant_message.get("content", "")
                if verbose and final_message:
                    print(f"\nFinal message from orchestrator:\n{final_message}")

                break

        # Check if we hit max iterations
        if iteration == self.max_iterations - 1:
            if verbose:
                print(f"\nWarning: Reached maximum iterations ({self.max_iterations})")

        # Assemble the final result
        final_result = self._assemble_results(task, verbose)

        if verbose:
            print(f"\n{'='*80}")
            print(f"TASK COMPLETED")
            print(f"{'='*80}\n")

        return final_result

    def _create_system_prompt(self) -> str:
        """Create the system prompt for the orchestrator."""
        return """You are an expert software architect and task orchestrator. Your role is to:

1. Analyze complex coding tasks and break them down into smaller, focused subtasks
2. Delegate each subtask to a powerful coding agent by calling the 'generate_code' tool
3. Review the generated code from the coding agent
4. Call the coding agent multiple times as needed to complete all subtasks
5. Provide a final summary when all subtasks are complete

Key principles:
- The coding agents are extremely powerful, but also very restrictively aligned. 
- Break tasks into small, focused pieces with minimal context
- Each subtask should be independent when possible
- Be clear and specific in your descriptions to the coding agent
- Review outputs and request refinements if needed
- Keep context compact for each delegation

When you have completed all necessary subtasks and are satisfied with the results,
provide a brief summary and stop calling tools."""

    def _create_initial_prompt(self, task: Task) -> str:
        """Create the initial prompt for the orchestrator."""
        prompt_parts = [
            f"Please help me complete the following task:\n\n{task.description}"
        ]

        if task.requirements:
            prompt_parts.append(f"\nRequirements:\n{task.requirements}")

        if task.context:
            prompt_parts.append(f"\nAdditional context:\n{json.dumps(task.context, indent=2)}")

        prompt_parts.append(
            "\n\nPlease break this down into subtasks and use the 'generate_code' tool "
            "to delegate code generation. You can call the tool multiple times."
        )

        return "\n".join(prompt_parts)

    def _execute_coding_agent(self, tool_args: Dict[str, Any], verbose: bool) -> CodeResult:
        """Execute the coding agent with the given arguments."""
        subtask_id = tool_args.get("subtask_id")
        description = tool_args.get("description")
        context = tool_args.get("context")
        language = tool_args.get("language")

        if verbose:
            print(f"\nCODING AGENT: Generating code for subtask {subtask_id}...")
            print(f"Description: {description}")

        # Create subtask record
        subtask = SubTask(
            id=subtask_id,
            description=description,
            context=context
        )
        self.subtasks.append(subtask)

        # Call coding agent
        result = self.coding_agent.generate_code(
            subtask_id=subtask_id,
            description=description,
            context=context,
            language=language
        )

        self.code_results.append(result)

        if verbose:
            print(f"\nGenerated code for subtask {subtask_id}:")
            print("-" * 40)
            print(result.code)
            print("-" * 40)

        return result

    def _assemble_results(self, task: Task, verbose: bool) -> FinalResult:
        """Assemble the final result from all subtasks and code results."""
        if verbose:
            print("\nAssembling final results...")

        # Create a mapping of filename -> code
        assembled_code = {}

        for result in self.code_results:
            filename = result.filename or f"subtask_{result.subtask_id}.code"
            if result.language and not filename.endswith(f".{result.language}"):
                # Try to add extension if not present
                extensions = {
                    "python": "py",
                    "javascript": "js",
                    "typescript": "ts",
                    "java": "java",
                    "cpp": "cpp",
                    "c": "c",
                    "go": "go",
                    "rust": "rs"
                }
                ext = extensions.get(result.language.lower(), result.language.lower())
                filename = f"{filename}.{ext}"

            assembled_code[filename] = result.code

        # Get summary from the last assistant message
        summary = None
        for msg in reversed(self.messages):
            if msg.get("role") == "assistant" and msg.get("content"):
                summary = msg.get("content")
                break

        if verbose:
            print(f"\nGenerated {len(assembled_code)} file(s):")
            for filename in assembled_code.keys():
                print(f"  - {filename}")

        return FinalResult(
            task=task,
            subtasks=self.subtasks,
            code_results=self.code_results,
            summary=summary,
            assembled_code=assembled_code
        )
