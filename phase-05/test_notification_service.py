"""
Test script for validating Notification Service functionality
"""
import json
from unittest.mock import MagicMock
from datetime import datetime
import uuid

from backend.notification_service.src.services.notification_service import NotificationService


def test_send_reminder_notification():
    """Test sending reminder notifications"""
    print("Testing reminder notification sending...")
    
    # Create NotificationService instance
    notification_service = NotificationService()
    
    # Create a sample reminder event
    event_data = {
        "id": str(uuid.uuid4()),
        "timestamp": datetime.now().isoformat(),
        "eventType": "reminder.triggered",
        "userId": str(uuid.uuid4()),
        "taskId": str(uuid.uuid4()),
        "payload": {
            "reminderId": str(uuid.uuid4()),
            "task": {
                "id": str(uuid.uuid4()),
                "userId": str(uuid.uuid4()),
                "title": "Meeting with Team",
                "description": "Weekly team sync meeting",
                "completed": False,
                "priority": 1,
                "dueDate": datetime.now().isoformat(),
                "createdAt": datetime.now().isoformat(),
                "updatedAt": datetime.now().isoformat(),
                "completedAt": None,
                "recurringRule": "",
                "parentTaskId": None
            }
        },
        "correlationId": str(uuid.uuid4()),
        "causationId": str(uuid.uuid4())
    }
    
    # Call the send_reminder_notification method
    notification_id = notification_service.send_reminder_notification(event_data)
    
    # Verify that the returned notification ID is a valid UUID
    assert isinstance(notification_id, uuid.UUID)
    
    print("✓ Reminder notification sending test passed")


def test_send_task_updated_notification():
    """Test sending task updated notifications"""
    print("Testing task updated notification sending...")
    
    # Create NotificationService instance
    notification_service = NotificationService()
    
    # Create a sample task updated event
    event_data = {
        "id": str(uuid.uuid4()),
        "timestamp": datetime.now().isoformat(),
        "eventType": "task.updated",
        "userId": str(uuid.uuid4()),
        "taskId": str(uuid.uuid4()),
        "payload": {
            "task": {
                "id": str(uuid.uuid4()),
                "userId": str(uuid.uuid4()),
                "title": "Updated Task",
                "description": "Updated task description",
                "completed": False,
                "priority": 2,
                "dueDate": datetime.now().isoformat(),
                "createdAt": datetime.now().isoformat(),
                "updatedAt": datetime.now().isoformat(),
                "completedAt": None,
                "recurringRule": "",
                "parentTaskId": None
            }
        },
        "correlationId": str(uuid.uuid4()),
        "causationId": str(uuid.uuid4())
    }
    
    # Call the send_task_updated_notification method
    notification_id = notification_service.send_task_updated_notification(event_data)
    
    # Verify that the returned notification ID is a valid UUID
    assert isinstance(notification_id, uuid.UUID)
    
    print("✓ Task updated notification sending test passed")


def test_send_task_created_notification():
    """Test sending task created notifications"""
    print("Testing task created notification sending...")
    
    # Create NotificationService instance
    notification_service = NotificationService()
    
    # Create a sample task created event
    event_data = {
        "id": str(uuid.uuid4()),
        "timestamp": datetime.now().isoformat(),
        "eventType": "task.created",
        "userId": str(uuid.uuid4()),
        "taskId": str(uuid.uuid4()),
        "payload": {
            "task": {
                "id": str(uuid.uuid4()),
                "userId": str(uuid.uuid4()),
                "title": "New Task",
                "description": "New task description",
                "completed": False,
                "priority": 1,
                "dueDate": datetime.now().isoformat(),
                "createdAt": datetime.now().isoformat(),
                "updatedAt": datetime.now().isoformat(),
                "completedAt": None,
                "recurringRule": "",
                "parentTaskId": None
            }
        },
        "correlationId": str(uuid.uuid4()),
        "causationId": str(uuid.uuid4())
    }
    
    # Call the send_task_created_notification method
    notification_id = notification_service.send_task_created_notification(event_data)
    
    # Verify that the returned notification ID is a valid UUID
    assert isinstance(notification_id, uuid.UUID)
    
    print("✓ Task created notification sending test passed")


def run_notification_service_tests():
    """Run all Notification Service tests"""
    print("Starting Notification Service validation...")
    print("-" * 50)
    
    try:
        test_send_reminder_notification()
        test_send_task_updated_notification()
        test_send_task_created_notification()
        
        print("-" * 50)
        print("✓ All Notification Service tests passed!")
        return True
    except Exception as e:
        print(f"✗ Notification Service test failed: {str(e)}")
        return False


if __name__ == "__main__":
    success = run_notification_service_tests()
    if success:
        print("\n✓ Notification Service validation completed successfully")
    else:
        print("\n✗ Notification Service validation failed")