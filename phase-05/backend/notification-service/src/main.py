import json
import os
from datetime import datetime
import uuid

from dapr.ext.grpc import App, InvokeMethodRequest, InvokeMethodResponse
from dapr.clients import DaprClient
from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.orm import sessionmaker

from .services.notification_service import NotificationService


# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Initialize Dapr app
app = App()


@app.method(name='send-notification')
def send_notification(request: InvokeMethodRequest) -> InvokeMethodResponse:
    """
    Send a notification based on incoming reminder events
    """
    try:
        # Parse the incoming event data from the request
        event_data_str = request.data.value.decode('utf-8')  # Decode the binary data
        event_data = json.loads(event_data_str)

        # Process the reminder event to send notification
        with SessionLocal() as session:
            notification_service = NotificationService(session)
            message_id = notification_service.send_reminder_notification(event_data)

        # Return success response
        response_data = {
            "sent": True,
            "messageId": str(message_id),
            "message": "Notification sent successfully"
        }

        return InvokeMethodResponse(
            data=json.dumps(response_data),
            content_type='application/json'
        )
    except Exception as e:
        # Return error response
        error_response = {
            "sent": False,
            "error": str(e)
        }

        return InvokeMethodResponse(
            data=json.dumps(error_response),
            content_type='application/json'
        )


if __name__ == '__main__':
    # Initialize database tables
    SQLModel.metadata.create_all(bind=engine)

    # Run the Dapr app on port 50001
    app.run(50001)