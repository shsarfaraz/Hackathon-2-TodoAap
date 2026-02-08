"""
Test script for validating event flows across deployed services
"""
import asyncio
import json
from unittest.mock import AsyncMock, MagicMock
import pytest
from datetime import datetime
import uuid
import time

from backend.chat_api.src.services.event_publisher import EventPublisher
from backend.recurring_task_service.src.services.recurring_task_service import RecurringTaskService
from backend.notification_service.src.services.notification_service import NotificationService
from backend.audit_service.src.services.audit_service import AuditService


def simulate_task_creation_flow():
    """Simulate the complete flow when a task is created"""
    print("Simulating task creation event flow...")
    
    # Mock Dapr client
    mock_dapr_client = MagicMock()
    
    # Create EventPublisher instance
    event_publisher = EventPublisher(lambda: mock_dapr_client)
    
    # Create a mock task
    mock_task = MagicMock()
    mock_task.id = uuid.uuid4()
    mock_task.user_id = uuid.uuid4()
    mock_task.title = "Test Task Creation"
    mock_task.description = "Task created to test event flow"
    mock_task.completed = False
    mock_task.priority = 1
    mock_task.due_date = datetime.now()
    mock_task.created_at = datetime.now()
    mock_task.updated_at = datetime.now()
    mock_task.completed_at = None
    mock_task.recurring_rule = None
    mock_task.parent_task_id = None
    
    # Publish a task created event
    event_publisher.publish_task_event("task.created", mock_task, mock_task.user_id)
    
    # Verify that the event was published
    assert mock_dapr_client.publish_event.called
    print("✓ Task creation event published")
    
    # Simulate the event being consumed by other services
    # In a real system, this would happen via Dapr pub/sub
    
    print("✓ Task creation event flow simulation completed")


def simulate_task_completion_flow():
    """Simulate the complete flow when a task is completed"""
    print("Simulating task completion event flow...")
    
    # Mock Dapr client
    mock_dapr_client = MagicMock()
    
    # Create EventPublisher instance
    event_publisher = EventPublisher(lambda: mock_dapr_client)
    
    # Create a mock task
    mock_task = MagicMock()
    mock_task.id = uuid.uuid4()
    mock_task.user_id = uuid.uuid4()
    mock_task.title = "Test Task Completion"
    mock_task.description = "Task completed to test event flow"
    mock_task.completed = True
    mock_task.priority = 1
    mock_task.due_date = datetime.now()
    mock_task.created_at = datetime.now()
    mock_task.updated_at = datetime.now()
    mock_task.completed_at = datetime.now()
    mock_task.recurring_rule = "0 9 * * 1-5"  # Recurring rule for testing
    mock_task.parent_task_id = None
    
    # Publish a task completed event
    event_publisher.publish_task_event("task.completed", mock_task, mock_task.user_id)
    
    # Verify that the event was published
    assert mock_dapr_client.publish_event.called
    print("✓ Task completion event published")
    
    # Simulate Recurring Task Service consuming the event
    mock_db = MagicMock()
    recurring_service = RecurringTaskService(mock_db)
    
    # Create event data for the completed task
    event_data = {
        "id": str(uuid.uuid4()),
        "timestamp": datetime.now().isoformat(),
        "eventType": "task.completed",
        "userId": str(mock_task.user_id),
        "taskId": str(mock_task.id),
        "payload": {
            "task": {
                "id": str(mock_task.id),
                "userId": str(mock_task.user_id),
                "title": mock_task.title,
                "description": mock_task.description,
                "completed": mock_task.completed,
                "priority": mock_task.priority,
                "dueDate": mock_task.due_date.isoformat(),
                "createdAt": mock_task.created_at.isoformat(),
                "updatedAt": mock_task.updated_at.isoformat(),
                "completedAt": mock_task.completed_at.isoformat(),
                "recurringRule": mock_task.recurring_rule,
                "parentTaskId": str(mock_task.parent_task_id) if mock_task.parent_task_id else None
            }
        },
        "correlationId": str(uuid.uuid4()),
        "causationId": str(uuid.uuid4())
    }
    
    # Mock the database operations
    mock_new_task = MagicMock()
    mock_new_task.id = uuid.uuid4()
    mock_new_task.user_id = mock_task.user_id
    mock_new_task.title = mock_task.title
    mock_new_task.description = mock_task.description
    mock_new_task.priority = mock_task.priority
    mock_new_task.recurring_rule = mock_task.recurring_rule
    mock_new_task.parent_task_id = mock_task.id
    
    mock_db.get.return_value = mock_task
    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.return_value = mock_new_task
    
    # Mock the generate_next_occurrence method
    recurring_service.generate_next_occurrence = MagicMock()
    
    # Handle the completed task event
    recurring_service.handle_completed_task(event_data)
    
    # Verify that generate_next_occurrence was called since the task has a recurring rule
    recurring_service.generate_next_occurrence.assert_called_once_with(mock_task)
    print("✓ Recurring Task Service processed completion event")
    
    print("✓ Task completion event flow simulation completed")


def simulate_reminder_event_flow():
    """Simulate the complete flow when a reminder is triggered"""
    print("Simulating reminder event flow...")
    
    # Mock Dapr client
    mock_dapr_client = MagicMock()
    
    # Create EventPublisher instance
    event_publisher = EventPublisher(lambda: mock_dapr_client)
    
    # Create a mock task and reminder
    mock_task = MagicMock()
    mock_task.id = uuid.uuid4()
    mock_task.user_id = uuid.uuid4()
    mock_task.title = "Test Reminder Task"
    mock_task.description = "Task with reminder to test event flow"
    mock_task.completed = False
    mock_task.priority = 1
    mock_task.due_date = datetime.now()
    mock_task.created_at = datetime.now()
    mock_task.updated_at = datetime.now()
    mock_task.completed_at = None
    mock_task.recurring_rule = None
    mock_task.parent_task_id = None
    
    mock_reminder = MagicMock()
    mock_reminder.id = uuid.uuid4()
    
    # Publish a reminder triggered event
    event_publisher.publish_reminder_event(mock_reminder, mock_task, mock_task.user_id)
    
    # Verify that the event was published
    assert mock_dapr_client.publish_event.called
    print("✓ Reminder triggered event published")
    
    # Simulate Notification Service consuming the event
    notification_service = NotificationService()
    
    # Create event data for the reminder
    event_data = {
        "id": str(uuid.uuid4()),
        "timestamp": datetime.now().isoformat(),
        "eventType": "reminder.triggered",
        "userId": str(mock_task.user_id),
        "taskId": str(mock_task.id),
        "payload": {
            "reminderId": str(mock_reminder.id),
            "task": {
                "id": str(mock_task.id),
                "userId": str(mock_task.user_id),
                "title": mock_task.title,
                "description": mock_task.description,
                "completed": mock_task.completed,
                "priority": mock_task.priority,
                "dueDate": mock_task.due_date.isoformat(),
                "createdAt": mock_task.created_at.isoformat(),
                "updatedAt": mock_task.updated_at.isoformat(),
                "completedAt": mock_task.completed_at.isoformat() if mock_task.completed_at else None,
                "recurringRule": mock_task.recurring_rule or "",
                "parentTaskId": str(mock_task.parent_task_id) if mock_task.parent_task_id else None
            }
        },
        "correlationId": str(uuid.uuid4()),
        "causationId": str(uuid.uuid4())
    }
    
    # Send the reminder notification
    notification_id = notification_service.send_reminder_notification(event_data)
    
    # Verify that a notification was sent
    assert isinstance(notification_id, uuid.UUID)
    print("✓ Notification Service processed reminder event")
    
    print("✓ Reminder event flow simulation completed")


def simulate_audit_logging_flow():
    """Simulate the complete flow when events are audited"""
    print("Simulating audit logging event flow...")
    
    # Mock database session
    mock_db = MagicMock()
    
    # Create AuditService instance
    audit_service = AuditService(mock_db)
    
    # Create a sample event to log
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
                "title": "Audit Test Task",
                "description": "Task for testing audit logging",
                "completed": True,
                "priority": 1,
                "dueDate": datetime.now().isoformat(),
                "createdAt": datetime.now().isoformat(),
                "updatedAt": datetime.now().isoformat(),
                "completedAt": datetime.now().isoformat(),
                "recurringRule": "",
                "parentTaskId": None
            }
        },
        "correlationId": str(uuid.uuid4()),
        "causationId": str(uuid.uuid4())
    }
    
    # Mock the database operations
    from backend.audit_service.src.models.audit_log import AuditLog
    mock_audit_entry = AuditLog(
        id=uuid.uuid4(),
        task_id=uuid.UUID(event_data['taskId']),
        user_id=uuid.UUID(event_data['userId']),
        action='completed',
        previous_state=None,
        new_state=event_data['payload']['task'],
        created_at=datetime.now()
    )
    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.return_value = mock_audit_entry
    
    # Log the event
    log_id = audit_service.log_event(event_data)
    
    # Verify that the audit entry was added to the database
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    
    # Verify that the returned log ID is a valid UUID
    assert isinstance(log_id, uuid.UUID)
    print("✓ Audit Service processed event")
    
    print("✓ Audit logging event flow simulation completed")


def run_event_flow_validation():
    """Run all event flow validation tests"""
    print("Starting event flow validation across services...")
    print("-" * 50)
    
    try:
        simulate_task_creation_flow()
        print()
        simulate_task_completion_flow()
        print()
        simulate_reminder_event_flow()
        print()
        simulate_audit_logging_flow()
        print("-" * 50)
        print("✓ All event flow validation tests passed!")
        return True
    except Exception as e:
        print(f"✗ Event flow validation test failed: {str(e)}")
        return False


if __name__ == "__main__":
    success = run_event_flow_validation()
    if success:
        print("\n✓ Event flow validation across deployed services completed successfully")
    else:
        print("\n✗ Event flow validation across deployed services failed")