"""
Test script for validating Chat API Service functionality
"""
import asyncio
import json
from unittest.mock import AsyncMock, MagicMock, patch
import pytest
from datetime import datetime
import uuid

from backend.chat_api.src.services.task_service import TaskService
from backend.chat_api.src.services.event_publisher import EventPublisher
from backend.chat_api.src.models.task import Task, TaskBase


def test_create_task():
    """Test task creation functionality"""
    print("Testing task creation...")
    
    # Mock database session and Dapr client
    mock_db = MagicMock()
    mock_task = Task(
        id=uuid.uuid4(),
        user_id=uuid.uuid4(),
        title="Test Task",
        description="Test Description",
        priority=1,
        due_date=datetime.now()
    )
    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.return_value = None
    mock_db.get.return_value = mock_task
    
    # Mock Dapr client
    mock_dapr_client = MagicMock()
    
    # Create TaskService instance with mocked dependencies
    task_service = TaskService(
        db_getter=lambda: mock_db,
        dapr_client_getter=lambda: mock_dapr_client
    )
    
    # Create test task data
    task_data = TaskBase(
        title="Test Task",
        description="Test Description",
        priority=1,
        due_date=datetime.now()
    )
    
    # Test task creation
    user_id = uuid.uuid4()
    created_task = task_service.create_task(user_id, task_data)
    
    # Verify the task was created
    assert created_task.title == "Test Task"
    assert created_task.description == "Test Description"
    print("✓ Task creation test passed")


def test_event_publishing():
    """Test event publishing via Dapr"""
    print("Testing event publishing...")
    
    # Mock Dapr client
    mock_dapr_client = MagicMock()
    
    # Create EventPublisher instance
    event_publisher = EventPublisher(
        dapr_client_getter=lambda: mock_dapr_client
    )
    
    # Create a mock task
    mock_task = MagicMock()
    mock_task.id = uuid.uuid4()
    mock_task.user_id = uuid.uuid4()
    mock_task.title = "Test Task"
    mock_task.description = "Test Description"
    mock_task.completed = False
    mock_task.priority = 1
    mock_task.due_date = datetime.now()
    mock_task.created_at = datetime.now()
    mock_task.updated_at = datetime.now()
    mock_task.completed_at = None
    mock_task.recurring_rule = None
    mock_task.parent_task_id = None
    
    # Test publishing a task created event
    event_publisher.publish_task_event("task.created", mock_task, mock_task.user_id)
    
    # Verify that the Dapr client's publish_event method was called
    assert mock_dapr_client.publish_event.called
    print("✓ Event publishing test passed")


def test_toggle_completion():
    """Test toggling task completion"""
    print("Testing task completion toggle...")
    
    # Mock database session
    mock_db = MagicMock()
    mock_task = Task(
        id=uuid.uuid4(),
        user_id=uuid.uuid4(),
        title="Test Task",
        description="Test Description",
        completed=False,
        priority=1,
        due_date=datetime.now()
    )
    mock_db.get.return_value = mock_task
    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.return_value = mock_task
    
    # Mock Dapr client
    mock_dapr_client = MagicMock()
    
    # Create TaskService instance
    task_service = TaskService(
        db_getter=lambda: mock_db,
        dapr_client_getter=lambda: mock_dapr_client
    )
    
    # Test toggling completion
    user_id = mock_task.user_id
    toggled_task = task_service.toggle_task_completion(user_id, mock_task.id)
    
    # Verify the task completion was toggled
    assert toggled_task.completed == True
    print("✓ Task completion toggle test passed")


def run_chat_api_tests():
    """Run all Chat API Service tests"""
    print("Starting Chat API Service validation...")
    print("-" * 50)
    
    try:
        test_create_task()
        test_event_publishing()
        test_toggle_completion()
        
        print("-" * 50)
        print("✓ All Chat API Service tests passed!")
        return True
    except Exception as e:
        print(f"✗ Chat API Service test failed: {str(e)}")
        return False


if __name__ == "__main__":
    success = run_chat_api_tests()
    if success:
        print("\n✓ Chat API Service validation completed successfully")
    else:
        print("\n✗ Chat API Service validation failed")