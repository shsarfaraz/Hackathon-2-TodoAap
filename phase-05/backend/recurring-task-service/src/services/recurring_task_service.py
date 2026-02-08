from datetime import datetime, timedelta
from croniter import croniter
from typing import Optional
import uuid

from sqlmodel import Session, select
# Import from shared models instead of local models
from backend.shared.models.task import Task


class RecurringTaskService:
    def __init__(self, db_session: Session):
        self.db = db_session

    def handle_completed_task(self, event_data: dict):
        """
        Handle a task.completed event and generate the next occurrence if it's a recurring task
        """
        task_id = uuid.UUID(event_data['taskId'])
        user_id = uuid.UUID(event_data['userId'])

        # Get the completed task
        statement = select(Task).where(Task.id == task_id)
        result = self.db.exec(statement)
        task = result.first()

        if task and task.recurring_rule:
            # Generate the next occurrence based on the recurring rule
            self.generate_next_occurrence(task)

    def generate_next_occurrence(self, completed_task: Task):
        """
        Generate the next occurrence of a recurring task based on its recurring rule
        """
        if not completed_task.recurring_rule:
            return None

        # Parse the cron expression to determine the next occurrence
        current_time = datetime.now()
        cron_iter = croniter(completed_task.recurring_rule, current_time)
        next_run_time = cron_iter.get_next(datetime)

        # Create a new task with the same properties as the original
        new_task = Task(
            user_id=completed_task.user_id,
            title=completed_task.title,
            description=completed_task.description,
            priority=completed_task.priority,
            due_date=next_run_time,
            recurring_rule=completed_task.recurring_rule,
            parent_task_id=completed_task.id  # Link to the parent task
        )

        # Add the new task to the database
        self.db.add(new_task)
        self.db.commit()
        self.db.refresh(new_task)

        # Publish an event for the newly created recurring task
        self.publish_recurring_task_created_event(new_task, completed_task.id)

        return new_task

    def publish_recurring_task_created_event(self, new_task: Task, parent_task_id: uuid.UUID):
        """
        Publish an event when a recurring task is created
        """
        # In a real implementation, this would publish an event via Dapr
        # For now, we'll just log the event
        event_payload = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.now().isoformat(),
            "eventType": "task.recurring_created",
            "userId": str(new_task.user_id),
            "taskId": str(new_task.id),
            "payload": {
                "task": {
                    "id": str(new_task.id),
                    "userId": str(new_task.user_id),
                    "title": new_task.title,
                    "description": new_task.description or "",
                    "completed": new_task.completed,
                    "priority": new_task.priority,
                    "dueDate": new_task.due_date.isoformat() if new_task.due_date else None,
                    "createdAt": new_task.created_at.isoformat(),
                    "updatedAt": new_task.updated_at.isoformat(),
                    "completedAt": new_task.completed_at.isoformat() if new_task.completed_at else None,
                    "recurringRule": new_task.recurring_rule or "",
                    "parentTaskId": str(parent_task_id)
                },
                "parentTaskId": str(parent_task_id)
            },
            "correlationId": str(uuid.uuid4()),
            "causationId": str(uuid.uuid4())
        }

        # In a real implementation, we would publish this event via Dapr pub/sub
        # dapr_client.publish_event(pubsub_name='pubsub', topic_name='task-events', data=event_payload)
        print(f"Recurring task created event: {event_payload}")