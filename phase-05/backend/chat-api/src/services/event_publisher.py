import json
from datetime import datetime
import uuid
from typing import Optional, Dict, Any

from dapr.clients import DaprClient


class EventPublisher:
    def __init__(self, dapr_client_getter):
        self.get_dapr_client = dapr_client_getter

    def publish_task_event(self, event_type: str, task, user_id: uuid.UUID, previous_state: Optional[Dict] = None):
        """Publish a task-related event via Dapr pub/sub"""
        with self.get_dapr_client() as client:
            # Create event payload
            event_payload = {
                "id": str(uuid.uuid4()),
                "timestamp": datetime.now().isoformat(),
                "eventType": event_type,
                "userId": str(user_id),
                "taskId": str(task.id),
                "payload": {
                    "task": {
                        "id": str(task.id),
                        "userId": str(task.user_id),
                        "title": task.title,
                        "description": task.description or "",
                        "completed": task.completed,
                        "priority": task.priority,
                        "dueDate": task.due_date.isoformat() if task.due_date else None,
                        "createdAt": task.created_at.isoformat(),
                        "updatedAt": task.updated_at.isoformat(),
                        "completedAt": task.completed_at.isoformat() if task.completed_at else None,
                        "recurringRule": task.recurring_rule or "",
                        "parentTaskId": str(task.parent_task_id) if task.parent_task_id else None
                    }
                },
                "correlationId": str(uuid.uuid4()),
                "causationId": str(uuid.uuid4())
            }

            # Add changes to payload if this is an update event
            if event_type == "task.updated" and previous_state:
                # Calculate changes
                changes = {}
                current_task = event_payload["payload"]["task"]
                for key, prev_value in previous_state.items():
                    curr_value = current_task[key]
                    if prev_value != curr_value:
                        changes[key] = f"{prev_value} -> {curr_value}"
                event_payload["payload"]["changes"] = changes

            # Publish to the appropriate topic based on event type
            topic_name = "task-events"
            if event_type.startswith("reminder"):
                topic_name = "reminders"
            
            # Serialize the event
            event_data = json.dumps(event_payload)
            
            # Publish the event via Dapr pub/sub
            client.publish_event(
                pubsub_name='pubsub',  # This should match the Dapr component name
                topic_name=topic_name,
                data=event_data,
                data_content_type='application/json'
            )

    def publish_task_deleted_event(self, task_id: uuid.UUID, user_id: uuid.UUID):
        """Publish a task deleted event via Dapr pub/sub"""
        with self.get_dapr_client() as client:
            # Create event payload
            event_payload = {
                "id": str(uuid.uuid4()),
                "timestamp": datetime.now().isoformat(),
                "eventType": "task.deleted",
                "userId": str(user_id),
                "taskId": str(task_id),
                "payload": {
                    "taskId": str(task_id)
                },
                "correlationId": str(uuid.uuid4()),
                "causationId": str(uuid.uuid4())
            }

            # Serialize the event
            event_data = json.dumps(event_payload)
            
            # Publish the event via Dapr pub/sub
            client.publish_event(
                pubsub_name='pubsub',  # This should match the Dapr component name
                topic_name='task-events',
                data=event_data,
                data_content_type='application/json'
            )

    def publish_reminder_event(self, reminder, task, user_id: uuid.UUID):
        """Publish a reminder event via Dapr pub/sub"""
        with self.get_dapr_client() as client:
            # Create event payload
            event_payload = {
                "id": str(uuid.uuid4()),
                "timestamp": datetime.now().isoformat(),
                "eventType": "reminder.triggered",
                "userId": str(user_id),
                "taskId": str(task.id),
                "payload": {
                    "reminderId": str(reminder.id),
                    "task": {
                        "id": str(task.id),
                        "userId": str(task.user_id),
                        "title": task.title,
                        "description": task.description or "",
                        "completed": task.completed,
                        "priority": task.priority,
                        "dueDate": task.due_date.isoformat() if task.due_date else None,
                        "createdAt": task.created_at.isoformat(),
                        "updatedAt": task.updated_at.isoformat(),
                        "completedAt": task.completed_at.isoformat() if task.completed_at else None,
                        "recurringRule": task.recurring_rule or "",
                        "parentTaskId": str(task.parent_task_id) if task.parent_task_id else None
                    }
                },
                "correlationId": str(uuid.uuid4()),
                "causationId": str(uuid.uuid4())
            }

            # Serialize the event
            event_data = json.dumps(event_payload)
            
            # Publish the event via Dapr pub/sub
            client.publish_event(
                pubsub_name='pubsub',  # This should match the Dapr component name
                topic_name='reminders',
                data=event_data,
                data_content_type='application/json'
            )