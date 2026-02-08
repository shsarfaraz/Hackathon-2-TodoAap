import uuid
from datetime import datetime
from typing import Dict, Any, List

from sqlmodel import Session, select
# Import from the shared models instead of local models
from backend.shared.models.audit_log import AuditLog


class AuditService:
    def __init__(self, db_session: Session):
        self.db = db_session

    def log_event(self, event_data: Dict[str, Any]) -> uuid.UUID:
        """
        Log an event to the audit trail
        """
        # Extract relevant information from the event
        task_id = uuid.UUID(event_data['taskId'])
        user_id = uuid.UUID(event_data['userId'])
        event_type = event_data['eventType']
        payload = event_data.get('payload', {})

        # Create an audit log entry
        audit_entry = AuditLog(
            task_id=task_id,
            user_id=user_id,
            action=self.map_event_type_to_action(event_type),
            previous_state=payload.get('previous_state'),
            new_state=payload.get('task'),  # For most events, the current state is in the 'task' field
            metadata={
                'eventId': event_data.get('id'),
                'timestamp': event_data.get('timestamp'),
                'correlationId': event_data.get('correlationId'),
                'causationId': event_data.get('causationId')
            }
        )

        # Add to database
        self.db.add(audit_entry)
        self.db.commit()
        self.db.refresh(audit_entry)

        return audit_entry.id

    def get_audit_log_for_task(self, task_id: uuid.UUID) -> List[AuditLog]:
        """
        Get the audit log for a specific task
        """
        # Query the database for audit logs related to this task
        statement = select(AuditLog).where(AuditLog.task_id == task_id)
        audit_logs = self.db.exec(statement).all()

        return audit_logs

    def map_event_type_to_action(self, event_type: str) -> str:
        """
        Map event types to audit actions
        """
        event_to_action_map = {
            'task.created': 'created',
            'task.updated': 'updated',
            'task.completed': 'completed',
            'task.deleted': 'deleted',
            'task.recurring_created': 'recurring_created',
            'reminder.triggered': 'reminder_triggered'
        }

        return event_to_action_map.get(event_type, 'unknown')

    def get_audit_log_by_user(self, user_id: uuid.UUID) -> List[AuditLog]:
        """
        Get the audit log for a specific user
        """
        statement = select(AuditLog).where(AuditLog.user_id == user_id)
        audit_logs = self.db.exec(statement).all()

        return audit_logs

    def get_audit_log_by_action(self, action: str) -> List[AuditLog]:
        """
        Get audit logs for a specific action
        """
        statement = select(AuditLog).where(AuditLog.action == action)
        audit_logs = self.db.exec(statement).all()

        return audit_logs