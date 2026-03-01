"""
Pydantic models for the To-Do List App.

Defines request bodies, response schemas, and validation rules for tasks.
"""

from typing import Optional
from pydantic import BaseModel, field_validator


# ---------------------------------------------------------------------------
# Valid values
# ---------------------------------------------------------------------------
VALID_PRIORITIES = {"low", "medium", "high"}
VALID_STATUSES = {"todo", "in_progress", "done"}


# ---------------------------------------------------------------------------
# Request models
# ---------------------------------------------------------------------------

class TaskCreate(BaseModel):
    """Request body for creating a new task."""

    title: str
    description: Optional[str] = None
    priority: str = "medium"

    @field_validator("priority")
    @classmethod
    def validate_priority(cls, v: str) -> str:
        """Ensure priority is one of: low, medium, high."""
        if v not in VALID_PRIORITIES:
            raise ValueError(f"priority must be one of {sorted(VALID_PRIORITIES)}")
        return v


class TaskUpdate(BaseModel):
    """Request body for updating an existing task (all fields optional)."""

    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None

    @field_validator("priority")
    @classmethod
    def validate_priority(cls, v: Optional[str]) -> Optional[str]:
        """Ensure priority, when provided, is one of: low, medium, high."""
        if v is not None and v not in VALID_PRIORITIES:
            raise ValueError(f"priority must be one of {sorted(VALID_PRIORITIES)}")
        return v


class StatusUpdate(BaseModel):
    """Request body for updating a task's status."""

    status: str

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: str) -> str:
        """Ensure status is one of: todo, in_progress, done."""
        if v not in VALID_STATUSES:
            raise ValueError(f"status must be one of {sorted(VALID_STATUSES)}")
        return v


# ---------------------------------------------------------------------------
# Response models
# ---------------------------------------------------------------------------

class TaskResponse(BaseModel):
    """Full task representation returned by the API."""

    id: str
    title: str
    description: Optional[str]
    status: str
    priority: str
    created_at: str
    updated_at: str


class SummaryResponse(BaseModel):
    """Aggregate counts of tasks grouped by status."""

    total: int
    todo: int
    in_progress: int
    done: int
