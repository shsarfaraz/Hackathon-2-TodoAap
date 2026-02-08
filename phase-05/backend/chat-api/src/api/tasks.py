from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional, List
from sqlmodel import Session
import uuid

from ..models.task import Task, TaskBase
from ..services.task_service import TaskService
from ..main import get_db

router = APIRouter()

@router.get("/", response_model=List[Task])
async def get_tasks(
    status: Optional[str] = Query(None, regex="^(all|pending|completed)$"),
    priority: Optional[int] = Query(None, ge=0, le=2),
    db: Session = Depends(get_db)
):
    """Get all tasks for the authenticated user"""
    # In a real implementation, we would get the user from the JWT token
    # For now, we'll use a placeholder user_id
    user_id = uuid.uuid4()
    
    task_service = TaskService(lambda: db, lambda: None)
    return task_service.get_user_tasks(user_id, status, priority)


@router.post("/", response_model=Task)
async def create_task(task_data: TaskBase, db: Session = Depends(get_db)):
    """Create a new task for the authenticated user"""
    # In a real implementation, we would get the user from the JWT token
    # For now, we'll use a placeholder user_id
    user_id = uuid.uuid4()
    
    task_service = TaskService(lambda: db, lambda: None)
    return task_service.create_task(user_id, task_data)


@router.get("/{task_id}", response_model=Task)
async def get_task(task_id: uuid.UUID, db: Session = Depends(get_db)):
    """Get a specific task by ID"""
    # In a real implementation, we would get the user from the JWT token
    # For now, we'll use a placeholder user_id
    user_id = uuid.uuid4()
    
    task_service = TaskService(lambda: db, lambda: None)
    task = task_service.get_task_by_id(user_id, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/{task_id}", response_model=Task)
async def update_task(task_id: uuid.UUID, task_data: TaskBase, db: Session = Depends(get_db)):
    """Update an existing task"""
    # In a real implementation, we would get the user from the JWT token
    # For now, we'll use a placeholder user_id
    user_id = uuid.uuid4()
    
    task_service = TaskService(lambda: db, lambda: None)
    updated_task = task_service.update_task(user_id, task_id, task_data)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task


@router.delete("/{task_id}")
async def delete_task(task_id: uuid.UUID, db: Session = Depends(get_db)):
    """Delete a specific task"""
    # In a real implementation, we would get the user from the JWT token
    # For now, we'll use a placeholder user_id
    user_id = uuid.uuid4()
    
    task_service = TaskService(lambda: db, lambda: None)
    success = task_service.delete_task(user_id, task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}


@router.patch("/{task_id}/toggle-completion", response_model=Task)
async def toggle_task_completion(task_id: uuid.UUID, db: Session = Depends(get_db)):
    """Toggle the completion status of a task"""
    # In a real implementation, we would get the user from the JWT token
    # For now, we'll use a placeholder user_id
    user_id = uuid.uuid4()
    
    task_service = TaskService(lambda: db, lambda: None)
    task = task_service.toggle_task_completion(user_id, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task