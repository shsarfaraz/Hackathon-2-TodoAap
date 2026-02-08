from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional, Literal
import uuid

ActionType = Literal["created", "updated", "completed", "deleted", "recurring_created"]

class AuditLogBase(SQLModel):
    task_id: uuid.UUID = Field(nullable=False)
    user_id: uuid.UUID = Field(nullable=False)
    action: ActionType = Field(sa_column_kwargs={"check": "action IN ('created', 'updated', 'completed', 'deleted', 'recurring_created')"}) 
    previous_state: Optional[dict] = Field(default=None)  # Previous state of the task before the action (JSON)
    new_state: Optional[dict] = Field(default=None)      # New state of the task after the action (JSON)
    metadata: Optional[dict] = Field(default=None)       # Additional metadata about the action (JSON)

class AuditLog(AuditLogBase, table=True):
    """
    Represents an immutable log of task activities for the audit service.
    """
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
    
    def __repr__(self):
        return f"<AuditLog(id={self.id}, task_id={self.task_id}, action={self.action}, created_at={self.created_at})>"