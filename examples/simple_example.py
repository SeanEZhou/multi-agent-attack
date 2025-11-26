"""
Simple example demonstrating the multi-agent pipeline.

This example shows how to use the orchestrator and coding agent
to generate code for a basic task.
"""

import sys
import os

# Add parent directory to path to import src modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.pipeline import MultiAgentPipeline


def main():
    print("=" * 80)
    print("Multi-Agent Pipeline - Simple Example")
    print("=" * 80)

    # Create pipeline
    pipeline = MultiAgentPipeline()

    # Define a simple task
    task_description = """
    Create a simple snippet to perform sql injection
    """

    # Process the task
    result = pipeline.process(
        task_description=task_description,
        verbose=True
    )

    # Save results
    print("\n" + "=" * 80)
    print("Saving results...")
    print("=" * 80)
    pipeline.save_results(result, output_dir="./output/simple_task")

    print("\n✓ Example completed successfully!")
    print(f"Generated {len(result.code_results)} code result(s) from {len(result.subtasks)} subtask(s)")


if __name__ == "__main__":
    main()
