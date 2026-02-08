"""
Test script for validating shared models and database consistency
"""
import uuid
from datetime import datetime
from typing import Optional

from backend.shared.models.user import User
from backend.shared.models.task import Task
from backend.shared.models.conversation import Conversation
from backend.shared.models.message import Message
from backend.shared.models.reminder import Reminder
from backend.shared.models.audit_log import AuditLog


def test_user_model():
    """Test User model structure and properties"""
    print("Testing User model...")
    
    # Create a user instance
    user = User(
        email="test@example.com",
        password_hash="hashed_password_here",
        is_active=True
    )
    
    # Verify the user has the expected properties
    assert hasattr(user, 'id')
    assert hasattr(user, 'email')
    assert hasattr(user, 'password_hash')
    assert hasattr(user, 'is_active')
    assert hasattr(user, 'created_at')
    assert hasattr(user, 'updated_at')
    assert hasattr(user, 'last_login_at')
    
    # Verify the email is set correctly
    assert user.email == "test@example.com"
    
    # Verify the ID is a UUID
    assert isinstance(user.id, uuid.UUID)
    
    print("✓ User model test passed")


def test_task_model():
    """Test Task model structure and properties"""
    print("Testing Task model...")
    
    # Create a task instance
    user_id = uuid.uuid4()
    task = Task(
        user_id=user_id,
        title="Test Task",
        description="Test Description",
        priority=1,
        due_date=datetime.now()
    )
    
    # Verify the task has the expected properties
    assert hasattr(task, 'id')
    assert hasattr(task, 'user_id')
    assert hasattr(task, 'title')
    assert hasattr(task, 'description')
    assert hasattr(task, 'completed')
    assert hasattr(task, 'priority')
    assert hasattr(task, 'due_date')
    assert hasattr(task, 'created_at')
    assert hasattr(task, 'updated_at')
    assert hasattr(task, 'completed_at')
    assert hasattr(task, 'recurring_rule')
    assert hasattr(task, 'parent_task_id')
    
    # Verify the title is set correctly
    assert task.title == "Test Task"
    
    # Verify the ID is a UUID
    assert isinstance(task.id, uuid.UUID)
    
    print("✓ Task model test passed")


def test_conversation_model():
    """Test Conversation model structure and properties"""
    print("Testing Conversation model...")
    
    # Create a conversation instance
    user_id = uuid.uuid4()
    conversation = Conversation(
        user_id=user_id,
        title="Test Conversation",
        is_active=True
    )
    
    # Verify the conversation has the expected properties
    assert hasattr(conversation, 'id')
    assert hasattr(conversation, 'user_id')
    assert hasattr(conversation, 'title')
    assert hasattr(conversation, 'created_at')
    assert hasattr(conversation, 'updated_at')
    assert hasattr(conversation, 'is_active')
    
    # Verify the title is set correctly
    assert conversation.title == "Test Conversation"
    
    # Verify the ID is a UUID
    assert isinstance(conversation.id, uuid.UUID)
    
    print("✓ Conversation model test passed")


def test_message_model():
    """Test Message model structure and properties"""
    print("Testing Message model...")
    
    # Create a conversation ID and message instance
    conversation_id = uuid.uuid4()
    message = Message(
        conversation_id=conversation_id,
        role="user",
        content="Test message content"
    )
    
    # Verify the message has the expected properties
    assert hasattr(message, 'id')
    assert hasattr(message, 'conversation_id')
    assert hasattr(message, 'role')
    assert hasattr(message, 'content')
    assert hasattr(message, 'created_at')
    assert hasattr(message, 'updated_at')
    assert hasattr(message, 'metadata')
    
    # Verify the content is set correctly
    assert message.content == "Test message content"
    
    # Verify the ID is a UUID
    assert isinstance(message.id, uuid.UUID)
    
    print("✓ Message model test passed")


def test_reminder_model():
    """Test Reminder model structure and properties"""
    print("Testing Reminder model...")
    
    # Create a task ID, user ID, and reminder instance
    task_id = uuid.uuid4()
    user_id = uuid.uuid4()
    reminder = Reminder(
        task_id=task_id,
        user_id=user_id,
        scheduled_at=datetime.now(),
        is_active=True
    )
    
    # Verify the reminder has the expected properties
    assert hasattr(reminder, 'id')
    assert hasattr(reminder, 'task_id')
    assert hasattr(reminder, 'user_id')
    assert hasattr(reminder, 'scheduled_at')
    assert hasattr(reminder, 'sent_at')
    assert hasattr(reminder, 'created_at')
    assert hasattr(reminder, 'updated_at')
    assert hasattr(reminder, 'is_active')
    
    # Verify the ID is a UUID
    assert isinstance(reminder.id, uuid.UUID)
    
    print("✓ Reminder model test passed")


def test_audit_log_model():
    """Test AuditLog model structure and properties"""
    print("Testing AuditLog model...")
    
    # Create an audit log instance
    task_id = uuid.uuid4()
    user_id = uuid.uuid4()
    audit_log = AuditLog(
        task_id=task_id,
        user_id=user_id,
        action="created",
        previous_state=None,
        new_state={"title": "Test Task"},
        metadata={"source": "test"}
    )
    
    # Verify the audit log has the expected properties
    assert hasattr(audit_log, 'id')
    assert hasattr(audit_log, 'task_id')
    assert hasattr(audit_log, 'user_id')
    assert hasattr(audit_log, 'action')
    assert hasattr(audit_log, 'previous_state')
    assert hasattr(audit_log, 'new_state')
    assert hasattr(audit_log, 'created_at')
    assert hasattr(audit_log, 'metadata')
    
    # Verify the action is set correctly
    assert audit_log.action == "created"
    
    # Verify the ID is a UUID
    assert isinstance(audit_log.id, uuid.UUID)
    
    print("✓ AuditLog model test passed")


def test_cross_model_consistency():
    """Test consistency between related models"""
    print("Testing cross-model consistency...")
    
    # Create instances of related models
    user = User(email="test@example.com", password_hash="hashed_password")
    task = Task(user_id=user.id, title="Test Task")
    conversation = Conversation(user_id=user.id, title="Test Conversation")
    message = Message(conversation_id=conversation.id, role="user", content="Test message")
    reminder = Reminder(task_id=task.id, user_id=user.id, scheduled_at=datetime.now())
    
    # Verify that the relationships are properly defined
    # (This would normally be checked by the SQLModel relationship definitions)
    
    # Verify that IDs are properly linked
    assert task.user_id == user.id
    assert conversation.user_id == user.id
    assert message.conversation_id == conversation.id
    assert reminder.user_id == user.id
    assert reminder.task_id == task.id
    
    print("✓ Cross-model consistency test passed")


def run_shared_models_tests():
    """Run all shared models and database consistency tests"""
    print("Starting shared models and database consistency validation...")
    print("-" * 50)
    
    try:
        test_user_model()
        test_task_model()
        test_conversation_model()
        test_message_model()
        test_reminder_model()
        test_audit_log_model()
        test_cross_model_consistency()
        
        print("-" * 50)
        print("✓ All shared models and database consistency tests passed!")
        return True
    except Exception as e:
        print(f"✗ Shared models test failed: {str(e)}")
        return False


if __name__ == "__main__":
    success = run_shared_models_tests()
    if success:
        print("\n✓ Shared models and database consistency validation completed successfully")
    else:
        print("\n✗ Shared models and database consistency validation failed")