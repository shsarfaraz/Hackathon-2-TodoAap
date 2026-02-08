import json
import os
from datetime import datetime
from croniter import croniter
from datetime import timedelta
import uuid

from dapr.ext.grpc import App, InvokeMethodRequest, InvokeMethodResponse
from dapr.clients import DaprClient
from sqlmodel import SQLModel, create_engine, Session, select
from sqlalchemy.orm import sessionmaker

# Import from shared models instead of local models
from backend.shared.models.task import Task
# Import the recurring task service from the local services
from .services.recurring_task_service import RecurringTaskService


# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Initialize Dapr app
app = App()


@app.method(name='process-event')
def process_event(request: InvokeMethodRequest) -> InvokeMethodResponse:
    """
    Process incoming task events to handle recurring task logic
    """
    try:
        # Parse the incoming event data from the request
        event_data_str = request.data.value.decode('utf-8')  # Decode the binary data
        event_data = json.loads(event_data_str)

        # Check if this is a task.completed event
        if event_data.get('eventType') == 'task.completed':
            # Process the completed task to see if it's recurring
            with SessionLocal() as session:
                recurring_service = RecurringTaskService(session)
                recurring_service.handle_completed_task(event_data)

        # Return success response
        response_data = {
            "processed": True,
            "message": "Event processed successfully"
        }

        return InvokeMethodResponse(
            data=json.dumps(response_data),
            content_type='application/json'
        )
    except Exception as e:
        # Return error response
        error_response = {
            "processed": False,
            "error": str(e)
        }

        return InvokeMethodResponse(
            data=json.dumps(error_response),
            content_type='application/json'
        )


# Initialize database tables
def init_db():
    SQLModel.metadata.create_all(bind=engine)


if __name__ == '__main__':
    # Initialize database
    init_db()

    # Run the Dapr app on port 50001
    app.run(50001)