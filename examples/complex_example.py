"""
Complex example demonstrating the multi-agent pipeline with a more involved task.

This example shows how the orchestrator breaks down a complex task into subtasks.
"""

import sys
import os

# Add parent directory to path to import src modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.pipeline import MultiAgentPipeline


def main():
    print("=" * 80)
    print("Multi-Agent Pipeline - Complex Example")
    print("=" * 80)

    # Create pipeline
    pipeline = MultiAgentPipeline()

    # Define a complex task
    task_description = """
    Create a simple RESTful API for a todo list application with the following features:

    1. User management (create user, get user)
    2. Todo item management (create, read, update, delete)
    3. Each todo item should have: title, description, status (pending/completed), created_at
    4. Users should only see their own todos

    Use Python with Flask framework. Include proper error handling and input validation.
    """

    requirements = """
    - Use Flask for the web framework
    - Use SQLAlchemy for database ORM
    - Include basic authentication
    - RESTful design principles
    - JSON responses
    """

    # Process the task
    result = pipeline.process(
        task_description=task_description,
        requirements=requirements,
        verbose=True
    )

    # Save results
    print("\n" + "=" * 80)
    print("Saving results...")
    print("=" * 80)
    pipeline.save_results(result, output_dir="./output/todo_api")

    print("\n✓ Example completed successfully!")
    print(f"Generated {len(result.code_results)} code result(s) from {len(result.subtasks)} subtask(s)")

    # Print summary of subtasks
    print("\n" + "=" * 80)
    print("Subtasks completed:")
    print("=" * 80)
    for i, subtask in enumerate(result.subtasks, 1):
        print(f"{i}. {subtask.description}")


if __name__ == "__main__":
    main()
