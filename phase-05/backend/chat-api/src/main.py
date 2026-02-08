import asyncio
import json
import os
from datetime import datetime
from typing import Dict, Any, List
import uuid

from dapr.ext.grpc import App, InvokeMethodRequest, InvokeMethodResponse
from dapr.clients import DaprClient
from sqlmodel import SQLModel, create_engine, Session, select
from sqlalchemy.orm import sessionmaker

# Import shared models
from backend.shared.models.task import Task
from backend.shared.models.conversation import Conversation
from backend.shared.models.message import Message
from backend.shared.models.user import User

# Import shared services
from backend.shared.services.task_service import TaskService
from backend.shared.services.conversation_service import ConversationService
from backend.shared.services.message_service import MessageService
from backend.shared.services.event_publisher import EventPublisher


# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo-chatbot.db")
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Initialize Dapr app
app = App()

# Initialize services
task_service = TaskService()
conversation_service = ConversationService()
message_service = MessageService()
event_publisher = EventPublisher()


@app.method(name='create-task')
def create_task(request: InvokeMethodRequest) -> InvokeMethodResponse:
    """
    Create a new task via the chat API
    """
    try:
        # Parse the incoming request data
        request_data_str = request.data.value.decode('utf-8')
        request_data = json.loads(request_data_str)
        
        # Extract task information from the request
        user_id = uuid.UUID(request_data['userId'])
        title = request_data['title']
        description = request_data.get('description', '')
        priority = request_data.get('priority', 1)
        due_date_str = request_data.get('dueDate')
        recurring_rule = request_data.get('recurringRule', '')
        
        # Convert due date string to datetime object if provided
        due_date = None
        if due_date_str:
            due_date = datetime.fromisoformat(due_date_str.replace('Z', '+00:00'))
        
        # Create a new database session
        with SessionLocal() as session:
            # Create the task using the task service
            new_task = task_service.create_task(
                session=session,
                user_id=user_id,
                title=title,
                description=description,
                priority=priority,
                due_date=due_date,
                recurring_rule=recurring_rule
            )
            
            # Publish a task.created event via Dapr pub/sub
            event_data = {
                "id": str(uuid.uuid4()),
                "timestamp": datetime.now().isoformat(),
                "eventType": "task.created",
                "userId": str(user_id),
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
                        "parentTaskId": str(new_task.parent_task_id) if new_task.parent_task_id else None
                    }
                },
                "correlationId": str(uuid.uuid4()),
                "causationId": str(uuid.uuid4())
            }
            
            # Publish the event using Dapr
            with DaprClient() as client:
                client.publish_event(
                    pubsub_name='pubsub',
                    topic_name='task-events',
                    data=json.dumps(event_data),
                    data_content_type='application/json'
                )
        
        # Prepare the response data
        response_data = {
            "created": True,
            "taskId": str(new_task.id),
            "message": "Task created successfully"
        }
        
        # Return the response
        return InvokeMethodResponse(
            data=json.dumps(response_data),
            content_type='application/json'
        )
    except Exception as e:
        # Prepare error response
        error_response = {
            "created": False,
            "error": str(e)
        }
        
        # Return error response
        return InvokeMethodResponse(
            data=json.dumps(error_response),
            content_type='application/json'
        )


@app.method(name='get-tasks')
def get_tasks(request: InvokeMethodRequest) -> InvokeMethodResponse:
    """
    Get all tasks for a user
    """
    try:
        # Parse the incoming request data
        request_data_str = request.data.value.decode('utf-8')
        request_data = json.loads(request_data_str)
        
        # Extract user ID from the request
        user_id = uuid.UUID(request_data['userId'])
        
        # Create a new database session
        with SessionLocal() as session:
            # Get all tasks for the user using the task service
            tasks = task_service.get_tasks_by_user(session, user_id)
        
        # Prepare the response data
        response_data = {
            "tasks": [task.__dict__ for task in tasks]
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


@app.method(name='update-task')
def update_task(request: InvokeMethodRequest) -> InvokeMethodResponse:
    """
    Update an existing task
    """
    try:
        # Parse the incoming request data
        request_data_str = request.data.value.decode('utf-8')
        request_data = json.loads(request_data_str)
        
        # Extract task information from the request
        task_id = uuid.UUID(request_data['taskId'])
        user_id = uuid.UUID(request_data['userId'])
        updates = request_data.get('updates', {})
        
        # Create a new database session
        with SessionLocal() as session:
            # Update the task using the task service
            updated_task = task_service.update_task(session, task_id, user_id, updates)
            
            # Publish a task.updated event via Dapr pub/sub
            event_data = {
                "id": str(uuid.uuid4()),
                "timestamp": datetime.now().isoformat(),
                "eventType": "task.updated",
                "userId": str(user_id),
                "taskId": str(task_id),
                "payload": {
                    "task": {
                        "id": str(updated_task.id),
                        "userId": str(updated_task.user_id),
                        "title": updated_task.title,
                        "description": updated_task.description or "",
                        "completed": updated_task.completed,
                        "priority": updated_task.priority,
                        "dueDate": updated_task.due_date.isoformat() if updated_task.due_date else None,
                        "createdAt": updated_task.created_at.isoformat(),
                        "updatedAt": updated_task.updated_at.isoformat(),
                        "completedAt": updated_task.completed_at.isoformat() if updated_task.completed_at else None,
                        "recurringRule": updated_task.recurring_rule or "",
                        "parentTaskId": str(updated_task.parent_task_id) if updated_task.parent_task_id else None
                    },
                    "changes": updates  # Include the changes made to the task
                },
                "correlationId": str(uuid.uuid4()),
                "causationId": str(uuid.uuid4())
            }
            
            # Publish the event using Dapr
            with DaprClient() as client:
                client.publish_event(
                    pubsub_name='pubsub',
                    topic_name='task-events',
                    data=json.dumps(event_data),
                    data_content_type='application/json'
                )
        
        # Prepare the response data
        response_data = {
            "updated": True,
            "taskId": str(updated_task.id),
            "message": "Task updated successfully"
        }
        
        # Return the response
        return InvokeMethodResponse(
            data=json.dumps(response_data),
            content_type='application/json'
        )
    except Exception as e:
        # Prepare error response
        error_response = {
            "updated": False,
            "error": str(e)
        }
        
        # Return error response
        return InvokeMethodResponse(
            data=json.dumps(error_response),
            content_type='application/json'
        )


@app.method(name='complete-task')
def complete_task(request: InvokeMethodRequest) -> InvokeMethodResponse:
    """
    Mark a task as completed
    """
    try:
        # Parse the incoming request data
        request_data_str = request.data.value.decode('utf-8')
        request_data = json.loads(request_data_str)
        
        # Extract task information from the request
        task_id = uuid.UUID(request_data['taskId'])
        user_id = uuid.UUID(request_data['userId'])
        
        # Create a new database session
        with SessionLocal() as session:
            # Mark the task as completed using the task service
            completed_task = task_service.complete_task(session, task_id, user_id)
            
            # Publish a task.completed event via Dapr pub/sub
            event_data = {
                "id": str(uuid.uuid4()),
                "timestamp": datetime.now().isoformat(),
                "eventType": "task.completed",
                "userId": str(user_id),
                "taskId": str(task_id),
                "payload": {
                    "task": {
                        "id": str(completed_task.id),
                        "userId": str(completed_task.user_id),
                        "title": completed_task.title,
                        "description": completed_task.description or "",
                        "completed": completed_task.completed,
                        "priority": completed_task.priority,
                        "dueDate": completed_task.due_date.isoformat() if completed_task.due_date else None,
                        "createdAt": completed_task.created_at.isoformat(),
                        "updatedAt": completed_task.updated_at.isoformat(),
                        "completedAt": completed_task.completed_at.isoformat() if completed_task.completed_at else None,
                        "recurringRule": completed_task.recurring_rule or "",
                        "parentTaskId": str(completed_task.parent_task_id) if completed_task.parent_task_id else None
                    }
                },
                "correlationId": str(uuid.uuid4()),
                "causationId": str(uuid.uuid4())
            }
            
            # Publish the event using Dapr
            with DaprClient() as client:
                client.publish_event(
                    pubsub_name='pubsub',
                    topic_name='task-events',
                    data=json.dumps(event_data),
                    data_content_type='application/json'
                )
        
        # Prepare the response data
        response_data = {
            "completed": True,
            "taskId": str(completed_task.id),
            "message": "Task completed successfully"
        }
        
        # Return the response
        return InvokeMethodResponse(
            data=json.dumps(response_data),
            content_type='application/json'
        )
    except Exception as e:
        # Prepare error response
        error_response = {
            "completed": False,
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