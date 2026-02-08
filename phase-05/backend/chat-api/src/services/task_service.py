from typing import Optional, List
from sqlmodel import Session, select
from datetime import datetime
import uuid

from ..models.task import Task, TaskBase
from ..models.user import User
from ..models.audit_log import AuditLog
from .event_publisher import EventPublisher


class TaskService:
    def __init__(self, db_getter, dapr_client_getter):
        self.get_db = db_getter
        self.get_dapr_client = dapr_client_getter
        self.event_publisher = EventPublisher(dapr_client_getter)

    def create_task(self, user_id: uuid.UUID, task_data: TaskBase) -> Task:
        """Create a new task for a user"""
        with self.get_db() as db:
            # Create the task
            task = Task(
                user_id=user_id,
                title=task_data.title,
                description=task_data.description,
                priority=task_data.priority,
                due_date=task_data.due_date,
                recurring_rule=task_data.recurring_rule
            )
            
            db.add(task)
            db.commit()
            db.refresh(task)
            
            # Publish task created event
            self.event_publisher.publish_task_event("task.created", task, user_id)
            
            return task

    def get_user_tasks(self, user_id: uuid.UUID, status: Optional[str] = None, priority: Optional[int] = None) -> List[Task]:
        """Get all tasks for a user with optional filtering"""
        with self.get_db() as db:
            query = select(Task).where(Task.user_id == user_id)
            
            if status:
                if status == "completed":
                    query = query.where(Task.completed == True)
                elif status == "pending":
                    query = query.where(Task.completed == False)
                    
            if priority is not None:
                query = query.where(Task.priority == priority)
                
            tasks = db.exec(query).all()
            return tasks

    def get_task_by_id(self, user_id: uuid.UUID, task_id: uuid.UUID) -> Optional[Task]:
        """Get a specific task by ID for a user"""
        with self.get_db() as db:
            task = db.get(Task, task_id)
            if task and task.user_id == user_id:
                return task
            return None

    def update_task(self, user_id: uuid.UUID, task_id: uuid.UUID, task_data: TaskBase) -> Optional[Task]:
        """Update an existing task"""
        with self.get_db() as db:
            task = db.get(Task, task_id)
            if task and task.user_id == user_id:
                # Store previous state for event
                previous_state = {
                    "id": str(task.id),
                    "userId": str(task.user_id),
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed,
                    "priority": task.priority,
                    "dueDate": task.due_date.isoformat() if task.due_date else None,
                    "createdAt": task.created_at.isoformat(),
                    "updatedAt": task.updated_at.isoformat(),
                    "completedAt": task.completed_at.isoformat() if task.completed_at else None,
                    "recurringRule": task.recurring_rule,
                    "parentTaskId": str(task.parent_task_id) if task.parent_task_id else None
                }
                
                # Update task
                task.title = task_data.title or task.title
                task.description = task_data.description or task.description
                task.priority = task_data.priority if task_data.priority is not None else task.priority
                task.due_date = task_data.due_date if task_data.due_date is not None else task.due_date
                task.recurring_rule = task_data.recurring_rule if task_data.recurring_rule is not None else task.recurring_rule
                task.updated_at = datetime.now()
                
                db.add(task)
                db.commit()
                db.refresh(task)
                
                # Publish task updated event
                self.event_publisher.publish_task_event("task.updated", task, user_id, previous_state)
                
                return task
            return None

    def delete_task(self, user_id: uuid.UUID, task_id: uuid.UUID) -> bool:
        """Delete a task"""
        with self.get_db() as db:
            task = db.get(Task, task_id)
            if task and task.user_id == user_id:
                # Publish task deleted event before deletion
                self.event_publisher.publish_task_deleted_event(task_id, user_id)
                
                db.delete(task)
                db.commit()
                return True
            return False

    def toggle_task_completion(self, user_id: uuid.UUID, task_id: uuid.UUID) -> Optional[Task]:
        """Toggle the completion status of a task"""
        with self.get_db() as db:
            task = db.get(Task, task_id)
            if task and task.user_id == user_id:
                # Store previous state for event
                previous_state = {
                    "id": str(task.id),
                    "userId": str(task.user_id),
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed,
                    "priority": task.priority,
                    "dueDate": task.due_date.isoformat() if task.due_date else None,
                    "createdAt": task.created_at.isoformat(),
                    "updatedAt": task.updated_at.isoformat(),
                    "completedAt": task.completed_at.isoformat() if task.completed_at else None,
                    "recurringRule": task.recurring_rule,
                    "parentTaskId": str(task.parent_task_id) if task.parent_task_id else None
                }
                
                # Toggle completion
                task.completed = not task.completed
                task.completed_at = datetime.now() if task.completed else None
                task.updated_at = datetime.now()
                
                db.add(task)
                db.commit()
                db.refresh(task)
                
                # Publish task completed event if task is now completed
                if task.completed:
                    self.event_publisher.publish_task_event("task.completed", task, user_id, previous_state)
                else:
                    # Publish task updated event if task is now incomplete
                    self.event_publisher.publish_task_event("task.updated", task, user_id, previous_state)
                
                return task
            return None