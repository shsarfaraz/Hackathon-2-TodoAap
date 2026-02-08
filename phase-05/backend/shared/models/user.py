from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
import uuid

class UserBase(SQLModel):
    email: str = Field(unique=True, nullable=False)
    is_active: bool = Field(default=True)

class User(UserBase, table=True):
    """
    Represents a registered user of the system.
    """
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    password_hash: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.now, nullable=False)
    last_login_at: Optional[datetime] = Field(default=None)
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"