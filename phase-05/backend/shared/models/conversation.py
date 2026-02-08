from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List
import uuid

class ConversationBase(SQLModel):
    title: str = Field(nullable=False, max_length=255)
    is_active: bool = Field(default=True)

class Conversation(ConversationBase, table=True):
    """
    Represents a conversation between the user and the AI assistant.
    """
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False)
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.now, nullable=False)
    
    # Relationships
    user: "User" = Relationship(back_populates="conversations")
    messages: List["Message"] = Relationship(back_populates="conversation")
    
    def __repr__(self):
        return f"<Conversation(id={self.id}, title={self.title})>"