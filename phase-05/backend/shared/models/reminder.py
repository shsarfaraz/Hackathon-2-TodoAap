from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional
import uuid

class ReminderBase(SQLModel):
    scheduled_at: datetime = Field(nullable=False)
    is_active: bool = Field(default=True)

class Reminder(ReminderBase, table=True):
    """
    Represents a scheduled reminder for a task.
    """
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    task_id: uuid.UUID = Field(foreign_key="task.id", nullable=False)
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False)
    sent_at: Optional[datetime] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.now, nullable=False)
    
    # Relationships
    task: "Task" = Relationship(back_populates="reminders")
    user: "User" = Relationship()
    
    def __repr__(self):
        return f"<Reminder(id={self.id}, task_id={self.task_id}, scheduled_at={self.scheduled_at})>"