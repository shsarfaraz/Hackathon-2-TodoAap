"""
Test script for validating Recurring Task Service functionality
"""
import json
from unittest.mock import MagicMock
from datetime import datetime, timedelta
import uuid

from backend.recurring_task_service.src.services.recurring_task_service import RecurringTaskService
from backend.recurring_task_service.src.models.task import Task


def test_handle_completed_task():
    """Test handling of completed task events"""
    print("Testing completed task event handling...")
    
    # Mock database session
    mock_db = MagicMock()
    
    # Create RecurringTaskService instance
    recurring_service = RecurringTaskService(mock_db)
    
    # Create a sample event data for a completed recurring task
    event_data = {
        "id": str(uuid.uuid4()),
        "timestamp": datetime.now().isoformat(),
        "eventType": "task.completed",
        "userId": str(uuid.uuid4()),
        "taskId": str(uuid.uuid4()),
        "payload": {
            "task": {
                "id": str(uuid.uuid4()),
                "userId": str(uuid.uuid4()),
                "title": "Daily Standup Meeting",
                "description": "Daily team standup meeting",
                "completed": True,
                "priority": 1,
                "dueDate": datetime.now().isoformat(),
                "createdAt": datetime.now().isoformat(),
                "updatedAt": datetime.now().isoformat(),
                "completedAt": datetime.now().isoformat(),
                "recurringRule": "0 9 * * 1-5",  # Every weekday at 9 AM
                "parentTaskId": None
            }
        },
        "correlationId": str(uuid.uuid4()),
        "causationId": str(uuid.uuid4())
    }
    
    # Mock the database get method to return a task with a recurring rule
    mock_task = MagicMock()
    mock_task.id = uuid.UUID(event_data['taskId'])
    mock_task.user_id = uuid.UUID(event_data['payload']['task']['userId'])
    mock_task.title = event_data['payload']['task']['title']
    mock_task.description = event_data['payload']['task']['description']
    mock_task.completed = event_data['payload']['task']['completed']
    mock_task.priority = event_data['payload']['task']['priority']
    mock_task.due_date = datetime.fromisoformat(event_data['payload']['task']['dueDate'].replace('Z', '+00:00'))
    mock_task.created_at = datetime.fromisoformat(event_data['payload']['task']['createdAt'].replace('Z', '+00:00'))
    mock_task.updated_at = datetime.fromisoformat(event_data['payload']['task']['updatedAt'].replace('Z', '+00:00'))
    mock_task.completed_at = datetime.fromisoformat(event_data['payload']['task']['completedAt'].replace('Z', '+00:00'))
    mock_task.recurring_rule = event_data['payload']['task']['recurringRule']
    mock_task.parent_task_id = None
    
    mock_db.get.return_value = mock_task
    
    # Mock the generate_next_occurrence method to prevent actual database operations
    recurring_service.generate_next_occurrence = MagicMock()
    
    # Call the handle_completed_task method
    recurring_service.handle_completed_task(event_data)
    
    # Verify that generate_next_occurrence was called since the task has a recurring rule
    recurring_service.generate_next_occurrence.assert_called_once_with(mock_task)
    
    print("✓ Completed task event handling test passed")


def test_generate_next_occurrence():
    """Test generation of next occurrence for recurring tasks"""
    print("Testing next occurrence generation...")
    
    # Mock database session
    mock_db = MagicMock()
    
    # Create RecurringTaskService instance
    recurring_service = RecurringTaskService(mock_db)
    
    # Create a mock completed task with a recurring rule
    completed_task = MagicMock()
    completed_task.id = uuid.uuid4()
    completed_task.user_id = uuid.uuid4()
    completed_task.title = "Daily Exercise"
    completed_task.description = "Morning exercise routine"
    completed_task.priority = 1
    completed_task.due_date = datetime.now()
    completed_task.recurring_rule = "0 7 * * *"  # Every day at 7 AM
    completed_task.parent_task_id = None
    
    # Mock the database operations
    mock_new_task = MagicMock()
    mock_new_task.id = uuid.uuid4()
    mock_new_task.user_id = completed_task.user_id
    mock_new_task.title = completed_task.title
    mock_new_task.description = completed_task.description
    mock_new_task.priority = completed_task.priority
    mock_new_task.recurring_rule = completed_task.recurring_rule
    mock_new_task.parent_task_id = completed_task.id
    
    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.return_value = mock_new_task
    
    # Mock the publish_recurring_task_created_event method
    recurring_service.publish_recurring_task_created_event = MagicMock()
    
    # Call the generate_next_occurrence method
    result = recurring_service.generate_next_occurrence(completed_task)
    
    # Verify that the new task was added to the database
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    
    # Verify that the event publishing method was called
    recurring_service.publish_recurring_task_created_event.assert_called_once()
    
    print("✓ Next occurrence generation test passed")


def test_non_recurring_task():
    """Test that non-recurring tasks don't generate new occurrences"""
    print("Testing non-recurring task handling...")
    
    # Mock database session
    mock_db = MagicMock()
    
    # Create RecurringTaskService instance
    recurring_service = RecurringTaskService(mock_db)
    
    # Create a sample event data for a completed non-recurring task
    event_data = {
        "id": str(uuid.uuid4()),
        "timestamp": datetime.now().isoformat(),
        "eventType": "task.completed",
        "userId": str(uuid.uuid4()),
        "taskId": str(uuid.uuid4()),
        "payload": {
            "task": {
                "id": str(uuid.uuid4()),
                "userId": str(uuid.uuid4()),
                "title": "Buy Groceries",
                "description": "Weekly grocery shopping",
                "completed": True,
                "priority": 1,
                "dueDate": datetime.now().isoformat(),
                "createdAt": datetime.now().isoformat(),
                "updatedAt": datetime.now().isoformat(),
                "completedAt": datetime.now().isoformat(),
                "recurringRule": "",  # No recurring rule
                "parentTaskId": None
            }
        },
        "correlationId": str(uuid.uuid4()),
        "causationId": str(uuid.uuid4())
    }
    
    # Mock the database get method to return a task without a recurring rule
    mock_task = MagicMock()
    mock_task.id = uuid.UUID(event_data['taskId'])
    mock_task.user_id = uuid.UUID(event_data['payload']['task']['userId'])
    mock_task.title = event_data['payload']['task']['title']
    mock_task.description = event_data['payload']['task']['description']
    mock_task.completed = event_data['payload']['task']['completed']
    mock_task.priority = event_data['payload']['task']['priority']
    mock_task.due_date = datetime.fromisoformat(event_data['payload']['task']['dueDate'].replace('Z', '+00:00'))
    mock_task.created_at = datetime.fromisoformat(event_data['payload']['task']['createdAt'].replace('Z', '+00:00'))
    mock_task.updated_at = datetime.fromisoformat(event_data['payload']['task']['updatedAt'].replace('Z', '+00:00'))
    mock_task.completed_at = datetime.fromisoformat(event_data['payload']['task']['completedAt'].replace('Z', '+00:00'))
    mock_task.recurring_rule = ""  # No recurring rule
    mock_task.parent_task_id = None
    
    mock_db.get.return_value = mock_task
    
    # Mock the generate_next_occurrence method
    recurring_service.generate_next_occurrence = MagicMock()
    
    # Call the handle_completed_task method
    recurring_service.handle_completed_task(event_data)
    
    # Verify that generate_next_occurrence was NOT called since the task has no recurring rule
    recurring_service.generate_next_occurrence.assert_not_called()
    
    print("✓ Non-recurring task handling test passed")


def run_recurring_task_service_tests():
    """Run all Recurring Task Service tests"""
    print("Starting Recurring Task Service validation...")
    print("-" * 50)
    
    try:
        test_handle_completed_task()
        test_generate_next_occurrence()
        test_non_recurring_task()
        
        print("-" * 50)
        print("✓ All Recurring Task Service tests passed!")
        return True
    except Exception as e:
        print(f"✗ Recurring Task Service test failed: {str(e)}")
        return False


if __name__ == "__main__":
    success = run_recurring_task_service_tests()
    if success:
        print("\n✓ Recurring Task Service validation completed successfully")
    else:
        print("\n✗ Recurring Task Service validation failed")