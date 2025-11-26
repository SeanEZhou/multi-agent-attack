from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class SubTask(BaseModel):
    """Represents a subtask created by the orchestrator."""
    id: int
    description: str
    context: Optional[str] = None
    dependencies: List[int] = Field(default_factory=list)


class CodeResult(BaseModel):
    """Represents the output from the coding agent."""
    subtask_id: int
    code: str
    explanation: Optional[str] = None
    language: Optional[str] = None
    filename: Optional[str] = None


class Task(BaseModel):
    """Represents the main task given by the user."""
    description: str
    requirements: Optional[str] = None
    context: Optional[Dict[str, Any]] = None


class FinalResult(BaseModel):
    """Represents the final result from the orchestrator."""
    task: Task
    subtasks: List[SubTask]
    code_results: List[CodeResult]
    summary: Optional[str] = None
