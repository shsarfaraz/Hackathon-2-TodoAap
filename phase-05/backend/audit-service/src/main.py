import json
import os
from contextlib import contextmanager
from datetime import datetime
from typing import Optional
import uuid

from dapr.ext.grpc import App, InvokeMethodRequest, InvokeMethodResponse
from dapr.clients import DaprClient
from sqlmodel import SQLModel, create_engine, Session, Field
from sqlalchemy.orm import sessionmaker

# Import the audit log model from shared models
from backend.shared.models.audit_log import AuditLog
# Import the audit service from the local services
from .services.audit_service import AuditService


# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Initialize Dapr app
app = App()


@app.method(name='log-event')
def log_event(request: InvokeMethodRequest) -> InvokeMethodResponse:
    """
    Log incoming task events to maintain an immutable audit trail
    """
    try:
        # Parse the incoming event data from the request
        event_data_str = request.data.value.decode('utf-8')  # Decode the binary data
        event_data = json.loads(event_data_str)

        # Create a new database session
        with SessionLocal() as session:
            # Create audit service instance
            audit_service = AuditService(session)
            # Log the event and get the log ID
            log_id = audit_service.log_event(event_data)

        # Prepare the response data
        response_data = {
            "logged": True,
            "logId": str(log_id),
            "message": "Event logged successfully"
        }

        # Return the response
        return InvokeMethodResponse(
            data=json.dumps(response_data),
            content_type='application/json'
        )
    except Exception as e:
        # Prepare error response
        error_response = {
            "logged": False,
            "error": str(e)
        }

        # Return error response
        return InvokeMethodResponse(
            data=json.dumps(error_response),
            content_type='application/json'
        )


@app.method(name='get-audit-log')
def get_audit_log(request: InvokeMethodRequest) -> InvokeMethodResponse:
    """
    Get audit log for a specific task
    """
    try:
        # Parse the request data
        request_data_str = request.data.value.decode('utf-8')  # Decode the binary data
        request_data = json.loads(request_data_str)
        
        # Get the task ID from the request
        task_id = uuid.UUID(request_data.get('taskId'))

        # Create a new database session
        with SessionLocal() as session:
            # Create audit service instance
            audit_service = AuditService(session)
            # Get the audit log for the task
            audit_logs = audit_service.get_audit_log_for_task(task_id)

        # Prepare the response data
        response_data = {
            "auditLogs": [log.__dict__ for log in audit_logs]  # Convert to dict for JSON serialization
        }

        # Return the response
        return InvokeMethodResponse(
            data=json.dumps(response_data),
            content_type='application/json'
        )
    except Exception as e:
        # Prepare error response
        error_response = {
            "error": str(e)
        }

        # Return error response
        return InvokeMethodResponse(
            data=json.dumps(error_response),
            content_type='application/json'
        )


if __name__ == '__main__':
    # Initialize database tables
    SQLModel.metadata.create_all(bind=engine)

    # Run the Dapr app on port 50001
    app.run(50001)