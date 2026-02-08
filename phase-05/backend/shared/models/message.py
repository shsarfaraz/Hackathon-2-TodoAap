from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, Literal
import uuid
from pydantic import BaseModel

RoleType = Literal["user", "assistant", "system"]

class MessageBase(SQLModel):
    role: RoleType = Field(sa_column_kwargs={"check": "role IN ('user', 'assistant', 'system)"})
    content: str = Field(nullable=False)
    metadata: Optional[dict] = Field(default=None)

class Message(MessageBase, table=True):
    """
    Represents a message in a conversation.
    """
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    conversation_id: uuid.UUID = Field(foreign_key="conversation.id", nullable=False)
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.now, nullable=False)
    
    # Relationships
    conversation: "Conversation" = Relationship(back_populates="messages")
    
    def __repr__(self):
        return f"<Message(id={self.id}, role={self.role}, content_preview='{self.content[:50]}...')>"