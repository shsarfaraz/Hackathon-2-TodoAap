"""
Models for the Todo Evolution application.

This module defines the data structures used in the application,
including the Task model and any related data classes.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Task:
    """
    Represents a single todo task.

    Attributes:
        id: Unique identifier for the task
        title: Title of the task
        description: Detailed description of the task
        completed: Boolean indicating if the task is completed
        created_at: Timestamp when the task was created
        updated_at: Timestamp when the task was last updated
    """

    id: int
    title: str
    description: str
    completed: bool = False
    created_at: datetime = None
    updated_at: datetime = None

    def __post_init__(self):
        """Initialize timestamps if not provided."""
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = self.created_at

    def mark_complete(self) -> None:
        """Mark the task as complete and update the timestamp."""
        self.completed = True
        self.updated_at = datetime.now()

    def mark_incomplete(self) -> None:
        """Mark the task as incomplete and update the timestamp."""
        self.completed = False
        self.updated_at = datetime.now()

    def update(self, title: Optional[str] = None, description: Optional[str] = None) -> None:
        """
        Update the task details.

        Args:
            title: New title for the task (optional)
            description: New description for the task (optional)
        """
        if title is not None:
            self.title = title
        if description is not None:
            self.description = description
        self.updated_at = datetime.now()

    def __str__(self) -> str:
        """String representation of the task for display purposes."""
        status = "[X]" if self.completed else "[ ]"
        return f"{status} {self.id}: {self.title} - {self.description}"