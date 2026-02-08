from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional
import uuid

class TaskBase(SQLModel):
    title: str = Field(nullable=False, max_length=255)
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False)
    priority: int = Field(default=0, ge=0, le=2)  # 0: low, 1: medium, 2: high
    due_date: Optional[datetime] = Field(default=None)
    recurring_rule: Optional[str] = Field(default=None, max_length=255)  # Cron expression for recurring tasks

class Task(TaskBase, table=True):
    """
    Represents a task in the todo system.
    """
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False)
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.now, nullable=False)
    completed_at: Optional[datetime] = Field(default=None)
    parent_task_id: Optional[uuid.UUID] = Field(default=None, foreign_key="task.id")  # For recurring task instances
    
    # Relationships
    user: "User" = Relationship(back_populates="tasks")
    parent_task: Optional["Task"] = Relationship(back_populates="child_tasks")
    child_tasks: list["Task"] = Relationship(back_populates="parent_task")
    
    def __repr__(self):
        return f"<Task(id={self.id}, title={self.title}, completed={self.completed})>"