"""
End-to-end scenario tests for the Todo Chatbot system
"""
import asyncio
import json
from unittest.mock import AsyncMock, MagicMock
import pytest
from datetime import datetime
import uuid

from backend.chat_api.src.services.task_service import TaskService
from backend.chat_api.src.services.event_publisher import EventPublisher
from backend.recurring_task_service.src.services.recurring_task_service import RecurringTaskService
from backend.notification_service.src.services.notification_service import NotificationService
from backend.audit_service.src.services.audit_service import AuditService


def scenario_1_complete_task_lifecycle():
    """
    Scenario 1: Complete task lifecycle
    1. Create a task
    2. Update the task
    3. Complete the task
    4. Verify recurring task generation (if applicable)
    5. Verify notifications sent
    6. Verify audit logs created
    """
    print("Running scenario 1: Complete task lifecycle...")
    
    # Mock database session
    mock_db = MagicMock()
    
    # Mock Dapr client
    mock_dapr_client = MagicMock()
    
    # Create services
    task_service = TaskService(
        db_getter=lambda: mock_db,
        dapr_client_getter=lambda: mock_dapr_client
    )
    event_publisher = EventPublisher(lambda: mock_dapr_client)
    recurring_service = RecurringTaskService(mock_db)
    notification_service = NotificationService()
    audit_service = AuditService(mock_db)
    
    # Step 1: Create a task
    user_id = uuid.uuid4()
    task_data = MagicMock()
    task_data.title = "Complete Task Lifecycle Test"
    task_data.description = "Test task for complete lifecycle"
    task_data.priority = 1
    task_data.due_date = datetime.now()
    task_data.recurring_rule = "0 9 * * 1-5"  # Daily at 9 AM on weekdays
    
    # Mock the database operations for task creation
    created_task = MagicMock()
    created_task.id = uuid.uuid4()
    created_task.user_id = user_id
    created_task.title = task_data.title
    created_task.description = task_data.description
    created_task.priority = task_data.priority
    created_task.due_date = task_data.due_date
    created_task.recurring_rule = task_data.recurring_rule
    created_task.completed = False
    
    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.return_value = created_task
    mock_db.get.return_value = created_task
    
    # Create the task
    created_task = task_service.create_task(user_id, task_data)
    print("✓ Step 1: Task created")
    
    # Step 2: Update the task
    updated_task_data = MagicMock()
    updated_task_data.title = "Updated Complete Task Lifecycle Test"
    updated_task_data.description = "Updated test task for complete lifecycle"
    updated_task_data.priority = 2
    
    # Mock the database operations for task update
    updated_task = MagicMock()
    updated_task.id = created_task.id
    updated_task.user_id = user_id
    updated_task.title = updated_task_data.title
    updated_task.description = updated_task_data.description
    updated_task.priority = updated_task_data.priority
    updated_task.due_date = created_task.due_date
    updated_task.recurring_rule = created_task.recurring_rule
    updated_task.completed = False
    
    mock_db.refresh.return_value = updated_task
    
    # Update the task
    updated_task = task_service.update_task(user_id, created_task.id, updated_task_data)
    print("✓ Step 2: Task updated")
    
    # Step 3: Complete the task
    # Mock the database operations for task completion
    completed_task = MagicMock()
    completed_task.id = created_task.id
    completed_task.user_id = user_id
    completed_task.title = updated_task.title
    completed_task.description = updated_task.description
    completed_task.priority = updated_task.priority
    completed_task.due_date = updated_task.due_date
    completed_task.recurring_rule = updated_task.recurring_rule
    completed_task.completed = True
    completed_task.completed_at = datetime.now()
    
    mock_db.refresh.return_value = completed_task
    
    # Complete the task
    completed_task = task_service.toggle_task_completion(user_id, created_task.id)
    print("✓ Step 3: Task completed")
    
    # Step 4: Verify recurring task generation
    # This would normally happen when the recurring service processes the completion event
    # For this test, we'll simulate the recurring service's reaction to the event
    event_data = {
        "id": str(uuid.uuid4()),
        "timestamp": datetime.now().isoformat(),
        "eventType": "task.completed",
        "userId": str(user_id),
        "taskId": str(created_task.id),
        "payload": {
            "task": {
                "id": str(created_task.id),
                "userId": str(user_id),
                "title": completed_task.title,
                "description": completed_task.description,
                "completed": completed_task.completed,
                "priority": completed_task.priority,
                "dueDate": completed_task.due_date.isoformat(),
                "createdAt": datetime.now().isoformat(),
                "updatedAt": datetime.now().isoformat(),
                "completedAt": completed_task.completed_at.isoformat(),
                "recurringRule": completed_task.recurring_rule,
                "parentTaskId": None
            }
        },
        "correlationId": str(uuid.uuid4()),
        "causationId": str(uuid.uuid4())
    }
    
    # Mock the recurring task generation
    recurring_service.generate_next_occurrence = MagicMock()
    recurring_service.handle_completed_task(event_data)
    recurring_service.generate_next_occurrence.assert_called_once()
    print("✓ Step 4: Recurring task generation verified")
    
    # Step 5: Verify notifications would be sent
    # In a real system, the notification service would receive events via Dapr pub/sub
    # For this test, we'll simulate the notification service receiving a reminder event
    reminder_event_data = {
        "id": str(uuid.uuid4()),
        "timestamp": datetime.now().isoformat(),
        "eventType": "reminder.triggered",
        "userId": str(user_id),
        "taskId": str(created_task.id),
        "payload": {
            "reminderId": str(uuid.uuid4()),
            "task": {
                "id": str(created_task.id),
                "userId": str(user_id),
                "title": completed_task.title,
                "description": completed_task.description,
                "completed": completed_task.completed,
                "priority": completed_task.priority,
                "dueDate": completed_task.due_date.isoformat(),
                "createdAt": datetime.now().isoformat(),
                "updatedAt": datetime.now().isoformat(),
                "completedAt": completed_task.completed_at.isoformat(),
                "recurringRule": completed_task.recurring_rule,
                "parentTaskId": None
            }
        },
        "correlationId": str(uuid.uuid4()),
        "causationId": str(uuid.uuid4())
    }
    
    notification_id = notification_service.send_reminder_notification(reminder_event_data)
    assert isinstance(notification_id, uuid.UUID)
    print("✓ Step 5: Notifications verified")
    
    # Step 6: Verify audit logs created
    # In a real system, the audit service would receive events via Dapr pub/sub
    # For this test, we'll simulate the audit service receiving an event
    audit_event_data = {
        "id": str(uuid.uuid4()),
        "timestamp": datetime.now().isoformat(),
        "eventType": "task.completed",
        "userId": str(user_id),
        "taskId": str(created_task.id),
        "payload": {
            "task": {
                "id": str(created_task.id),
                "userId": str(user_id),
                "title": completed_task.title,
                "description": completed_task.description,
                "completed": completed_task.completed,
                "priority": completed_task.priority,
                "dueDate": completed_task.due_date.isoformat(),
                "createdAt": datetime.now().isoformat(),
                "updatedAt": datetime.now().isoformat(),
                "completedAt": completed_task.completed_at.isoformat(),
                "recurringRule": completed_task.recurring_rule,
                "parentTaskId": None
            }
        },
        "correlationId": str(uuid.uuid4()),
        "causationId": str(uuid.uuid4())
    }
    
    # Mock the database operations for audit logging
    from backend.audit_service.src.models.audit_log import AuditLog
    mock_audit_entry = AuditLog(
        id=uuid.uuid4(),
        task_id=uuid.UUID(audit_event_data['taskId']),
        user_id=uuid.UUID(audit_event_data['userId']),
        action='completed',
        previous_state=None,
        new_state=audit_event_data['payload']['task'],
        created_at=datetime.now()
    )
    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.return_value = mock_audit_entry
    
    log_id = audit_service.log_event(audit_event_data)
    assert isinstance(log_id, uuid.UUID)
    print("✓ Step 6: Audit logs verified")
    
    print("✓ Scenario 1 completed successfully")


def scenario_2_recurring_task_workflow():
    """
    Scenario 2: Recurring task workflow
    1. Create a recurring task
    2. Complete the task
    3. Verify next occurrence is generated
    4. Verify event flows correctly
    """
    print("Running scenario 2: Recurring task workflow...")
    
    # Mock database session
    mock_db = MagicMock()
    
    # Create RecurringTaskService instance
    recurring_service = RecurringTaskService(mock_db)
    
    # Step 1: Create a recurring task (simulated through event)
    # In a real system, this would come from the Chat API via Dapr pub/sub
    user_id = uuid.uuid4()
    task_id = uuid.uuid4()
    
    # Step 2: Complete the recurring task
    event_data = {
        "id": str(uuid.uuid4()),
        "timestamp": datetime.now().isoformat(),
        "eventType": "task.completed",
        "userId": str(user_id),
        "taskId": str(task_id),
        "payload": {
            "task": {
                "id": str(task_id),
                "userId": str(user_id),
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
    recurring_service.publish_recurring_task_created_event = MagicMock()
    
    # Call the handle_completed_task method
    recurring_service.handle_completed_task(event_data)
    
    # Step 3: Verify next occurrence is generated
    # Verify that generate_next_occurrence was called since the task has a recurring rule
    recurring_service.generate_next_occurrence.assert_called_once_with(mock_task)
    print("✓ Step 3: Next occurrence generation verified")
    
    # Step 4: Verify event flows correctly
    # The recurring task service would publish an event when it creates a new task
    recurring_service.publish_recurring_task_created_event.assert_called_once()
    print("✓ Step 4: Event flows verified")
    
    print("✓ Scenario 2 completed successfully")


def run_end_to_end_tests():
    """Run all end-to-end scenario tests"""
    print("Starting end-to-end scenario tests...")
    print("=" * 60)
    
    try:
        scenario_1_complete_task_lifecycle()
        print()
        scenario_2_recurring_task_workflow()
        print("=" * 60)
        print("✓ All end-to-end scenario tests passed!")
        return True
    except Exception as e:
        print(f"✗ End-to-end scenario test failed: {str(e)}")
        return False


if __name__ == "__main__":
    success = run_end_to_end_tests()
    if success:
        print("\n✓ End-to-end scenario tests completed successfully")
    else:
        print("\n✗ End-to-end scenario tests failed")