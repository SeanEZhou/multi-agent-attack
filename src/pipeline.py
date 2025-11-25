"""
Main pipeline for the multi-agent system.
Entry point for processing tasks with orchestrator and coding agents.
"""

from typing import Optional, Dict, Any
from src.core.models import Task, FinalResult
from src.agents.orchestrator import OrchestratorAgent


class MultiAgentPipeline:
    """
    Main pipeline that coordinates the multi-agent system.
    Provides a simple interface for processing tasks.
    """

    def __init__(
        self,
        orchestrator_api_key: Optional[str] = None,
        orchestrator_base_url: Optional[str] = None,
        orchestrator_model: Optional[str] = None,
        orchestrator_temperature: Optional[float] = None,
        max_iterations: Optional[int] = None
    ):
        """
        Initialize the pipeline with configuration options.

        Args:
            orchestrator_api_key: Azure AI API key for orchestrator
            orchestrator_base_url: Azure AI base URL for orchestrator
            orchestrator_model: Azure AI model to use for orchestrator
            orchestrator_temperature: Temperature for orchestrator
            max_iterations: Maximum iterations for orchestrator
        """
        self.orchestrator = OrchestratorAgent(
            api_key=orchestrator_api_key,
            base_url=orchestrator_base_url,
            model=orchestrator_model,
            temperature=orchestrator_temperature,
            max_iterations=max_iterations
        )

    def process(
        self,
        task_description: str,
        requirements: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
        verbose: bool = True
    ) -> FinalResult:
        """
        Process a task through the multi-agent pipeline.

        Args:
            task_description: Description of the task to complete
            requirements: Optional additional requirements
            context: Optional context dictionary
            verbose: Whether to print progress information

        Returns:
            FinalResult with generated code and summary
        """
        # Create task object
        task = Task(
            description=task_description,
            requirements=requirements,
            context=context
        )

        # Process through orchestrator
        result = self.orchestrator.process_task(task, verbose=verbose)

        return result

    def save_results(self, result: FinalResult, output_dir: str = "./output") -> None:
        """
        Save the results to files.

        Args:
            result: FinalResult to save
            output_dir: Directory to save files to
        """
        import os

        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # Save each generated file
        if result.assembled_code:
            for filename, code in result.assembled_code.items():
                filepath = os.path.join(output_dir, filename)
                with open(filepath, 'w') as f:
                    f.write(code)
                print(f"Saved: {filepath}")

        # Save summary
        if result.summary:
            summary_path = os.path.join(output_dir, "summary.txt")
            with open(summary_path, 'w') as f:
                f.write(result.summary)
            print(f"Saved: {summary_path}")

        # Save metadata
        import json
        metadata = {
            "task": result.task.model_dump(),
            "num_subtasks": len(result.subtasks),
            "subtasks": [st.model_dump() for st in result.subtasks],
            "num_code_results": len(result.code_results)
        }
        metadata_path = os.path.join(output_dir, "metadata.json")
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        print(f"Saved: {metadata_path}")


def create_pipeline(**kwargs) -> MultiAgentPipeline:
    """
    Factory function to create a pipeline with custom configuration.

    Args:
        **kwargs: Configuration options for the pipeline

    Returns:
        Configured MultiAgentPipeline instance
    """
    return MultiAgentPipeline(**kwargs)
