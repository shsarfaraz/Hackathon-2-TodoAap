"""
Test script for validating Audit Service functionality
"""
import json
from unittest.mock import MagicMock
from datetime import datetime
import uuid

from backend.audit_service.src.services.audit_service import AuditService
from backend.audit_service.src.models.audit_log import AuditLog


def test_log_event():
    """Test logging events to the audit trail"""
    print("Testing event logging to audit trail...")
    
    # Mock database session
    mock_db = MagicMock()
    
    # Create AuditService instance
    audit_service = AuditService(mock_db)
    
    # Create a sample event to log
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
                "title": "Audit Test Task",
                "description": "Task for testing audit logging",
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
    
    # Mock the database operations
    mock_audit_entry = AuditLog(
        id=uuid.uuid4(),
        task_id=uuid.UUID(event_data['taskId']),
        user_id=uuid.UUID(event_data['userId']),
        action='created',
        previous_state=None,
        new_state=event_data['payload']['task'],
        created_at=datetime.now()
    )
    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.return_value = mock_audit_entry
    
    # Call the log_event method
    log_id = audit_service.log_event(event_data)
    
    # Verify that the audit entry was added to the database
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    
    # Verify that the returned log ID is a valid UUID
    assert isinstance(log_id, uuid.UUID)
    
    print("✓ Event logging test passed")


def test_get_audit_log_for_task():
    """Test retrieving audit logs for a specific task"""
    print("Testing retrieval of audit logs for a task...")
    
    # Mock database session
    mock_db = MagicMock()
    
    # Create AuditService instance
    audit_service = AuditService(mock_db)
    
    # Create mock audit logs
    task_id = uuid.uuid4()
    mock_audit_logs = [
        AuditLog(
            id=uuid.uuid4(),
            task_id=task_id,
            user_id=uuid.uuid4(),
            action='created',
            previous_state=None,
            new_state={'title': 'Test Task'},
            created_at=datetime.now()
        ),
        AuditLog(
            id=uuid.uuid4(),
            task_id=task_id,
            user_id=uuid.uuid4(),
            action='updated',
            previous_state={'title': 'Test Task'},
            new_state={'title': 'Updated Test Task'},
            created_at=datetime.now()
        )
    ]
    
    # Mock the database query
    mock_statement = MagicMock()
    mock_exec_result = MagicMock()
    mock_exec_result.all.return_value = mock_audit_logs
    mock_db.exec.return_value = mock_exec_result
    
    # Call the get_audit_log_for_task method
    audit_logs = audit_service.get_audit_log_for_task(task_id)
    
    # Verify that the database query was executed
    mock_db.exec.assert_called_once()
    
    # Verify that the correct number of audit logs were returned
    assert len(audit_logs) == 2
    
    print("✓ Audit log retrieval test passed")


def test_event_type_mapping():
    """Test mapping of event types to audit actions"""
    print("Testing event type to action mapping...")
    
    # Mock database session
    mock_db = MagicMock()
    
    # Create AuditService instance
    audit_service = AuditService(mock_db)
    
    # Test various event types
    test_cases = [
        ("task.created", "created"),
        ("task.updated", "updated"),
        ("task.completed", "completed"),
        ("task.deleted", "deleted"),
        ("task.recurring_created", "recurring_created"),
        ("reminder.triggered", "reminder_triggered"),
        ("unknown.event", "unknown")
    ]
    
    for event_type, expected_action in test_cases:
        result = audit_service.map_event_type_to_action(event_type)
        assert result == expected_action, f"Expected {expected_action} for {event_type}, got {result}"
    
    print("✓ Event type mapping test passed")


def run_audit_service_tests():
    """Run all Audit Service tests"""
    print("Starting Audit Service validation...")
    print("-" * 50)
    
    try:
        test_log_event()
        test_get_audit_log_for_task()
        test_event_type_mapping()
        
        print("-" * 50)
        print("✓ All Audit Service tests passed!")
        return True
    except Exception as e:
        print(f"✗ Audit Service test failed: {str(e)}")
        return False


if __name__ == "__main__":
    success = run_audit_service_tests()
    if success:
        print("\n✓ Audit Service validation completed successfully")
    else:
        print("\n✗ Audit Service validation failed")