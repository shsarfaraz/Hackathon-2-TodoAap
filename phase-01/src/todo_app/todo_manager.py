"""
Todo Manager for the Todo Evolution application.

This module handles the core business logic for managing tasks,
including adding, deleting, updating, and viewing tasks.
"""

from typing import Dict, List, Optional
from .models import Task


class TodoManager:
    """
    Manages the collection of tasks in memory.

    This class provides methods to add, delete, update, and view tasks.
    All tasks are stored in memory and will be lost when the application closes.
    """

    def __init__(self):
        """Initialize the TodoManager with an empty task collection."""
        self._tasks: Dict[int, Task] = {}
        self._next_id = 1

    def add_task(self, title: str, description: str) -> Task:
        """
        Add a new task to the collection.

        Args:
            title: Title of the task
            description: Description of the task

        Returns:
            The newly created Task object
        """
        # Create a new task with the next available ID
        task = Task(
            id=self._next_id,
            title=title,
            description=description
        )

        # Add the task to the collection
        self._tasks[self._next_id] = task

        # Increment the next ID for the next task
        self._next_id += 1

        return task

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task by its ID.

        Args:
            task_id: ID of the task to delete

        Returns:
            True if the task was found and deleted, False otherwise
        """
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def update_task(self, task_id: int, title: Optional[str] = None,
                   description: Optional[str] = None) -> bool:
        """
        Update a task's details by its ID.

        Args:
            task_id: ID of the task to update
            title: New title for the task (optional)
            description: New description for the task (optional)

        Returns:
            True if the task was found and updated, False otherwise
        """
        if task_id in self._tasks:
            self._tasks[task_id].update(title, description)
            return True
        return False

    def get_task(self, task_id: int) -> Optional[Task]:
        """
        Get a specific task by its ID.

        Args:
            task_id: ID of the task to retrieve

        Returns:
            The Task object if found, None otherwise
        """
        return self._tasks.get(task_id)

    def get_all_tasks(self) -> List[Task]:
        """
        Get all tasks in the collection.

        Returns:
            A list of all Task objects
        """
        return list(self._tasks.values())

    def mark_task_complete(self, task_id: int) -> bool:
        """
        Mark a task as complete by its ID.

        Args:
            task_id: ID of the task to mark as complete

        Returns:
            True if the task was found and updated, False otherwise
        """
        task = self._tasks.get(task_id)
        if task:
            task.mark_complete()
            return True
        return False

    def mark_task_incomplete(self, task_id: int) -> bool:
        """
        Mark a task as incomplete by its ID.

        Args:
            task_id: ID of the task to mark as incomplete

        Returns:
            True if the task was found and updated, False otherwise
        """
        task = self._tasks.get(task_id)
        if task:
            task.mark_incomplete()
            return True
        return False

    def get_next_id(self) -> int:
        """
        Get the next available ID for a new task.

        Returns:
            The next available task ID
        """
        return self._next_id

    def get_tasks_by_status(self, completed: bool) -> List[Task]:
        """
        Get tasks filtered by completion status.

        Args:
            completed: True to get completed tasks, False to get pending tasks

        Returns:
            A list of Task objects matching the status
        """
        return [task for task in self._tasks.values() if task.completed == completed]

    def search_tasks(self, query: str) -> List[Task]:
        """
        Search tasks by title or description.

        Args:
            query: Search term to look for in task titles and descriptions

        Returns:
            A list of Task objects matching the search query
        """
        query_lower = query.lower()
        matching_tasks = []

        for task in self._tasks.values():
            if query_lower in task.title.lower() or query_lower in task.description.lower():
                matching_tasks.append(task)

        return matching_tasks