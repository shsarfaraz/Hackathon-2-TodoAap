"""
Basic tests for the Todo Evolution application.

This module contains unit tests for the core functionality of the todo app.
"""
import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.todo_app.models import Task
from src.todo_app.todo_manager import TodoManager


class TestTask:
    """Test cases for the Task model."""

    def test_task_creation(self):
        """Test that a task can be created with required attributes."""
        task = Task(id=1, title="Test Task", description="Test Description")

        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == "Test Description"
        assert task.completed is False

    def test_task_completion(self):
        """Test that a task can be marked as complete and incomplete."""
        task = Task(id=1, title="Test Task", description="Test Description")

        # Initially task should be incomplete
        assert task.completed is False

        # Mark as complete
        task.mark_complete()
        assert task.completed is True

        # Mark as incomplete
        task.mark_incomplete()
        assert task.completed is False

    def test_task_update(self):
        """Test that a task's details can be updated."""
        task = Task(id=1, title="Original Title", description="Original Description")

        # Update title and description
        task.update(title="New Title", description="New Description")

        assert task.title == "New Title"
        assert task.description == "New Description"

    def test_task_str_representation(self):
        """Test the string representation of a task."""
        task = Task(id=1, title="Test Task", description="Test Description")

        # Test incomplete task representation
        str_repr = str(task)
        assert "[ ]" in str_repr  # Incomplete indicator
        assert "1:" in str_repr
        assert "Test Task" in str_repr

        # Mark complete and test again
        task.mark_complete()
        str_repr = str(task)
        assert "[X]" in str_repr  # Complete indicator


class TestTodoManager:
    """Test cases for the TodoManager class."""

    def test_add_task(self):
        """Test that tasks can be added to the manager."""
        manager = TodoManager()

        task = manager.add_task("Test Title", "Test Description")

        assert task.id == 1
        assert task.title == "Test Title"
        assert task.description == "Test Description"
        assert len(manager.get_all_tasks()) == 1

    def test_get_task(self):
        """Test that tasks can be retrieved by ID."""
        manager = TodoManager()
        added_task = manager.add_task("Test Title", "Test Description")

        retrieved_task = manager.get_task(added_task.id)

        assert retrieved_task is not None
        assert retrieved_task.id == added_task.id
        assert retrieved_task.title == added_task.title

    def test_get_nonexistent_task(self):
        """Test that retrieving a non-existent task returns None."""
        manager = TodoManager()

        task = manager.get_task(999)

        assert task is None

    def test_get_all_tasks(self):
        """Test that all tasks can be retrieved."""
        manager = TodoManager()
        manager.add_task("Task 1", "Description 1")
        manager.add_task("Task 2", "Description 2")

        tasks = manager.get_all_tasks()

        assert len(tasks) == 2

    def test_delete_task(self):
        """Test that tasks can be deleted."""
        manager = TodoManager()
        task = manager.add_task("Test Title", "Test Description")

        result = manager.delete_task(task.id)

        assert result is True
        assert len(manager.get_all_tasks()) == 0

    def test_delete_nonexistent_task(self):
        """Test that deleting a non-existent task returns False."""
        manager = TodoManager()

        result = manager.delete_task(999)

        assert result is False

    def test_update_task(self):
        """Test that tasks can be updated."""
        manager = TodoManager()
        task = manager.add_task("Original Title", "Original Description")

        result = manager.update_task(task.id, "New Title", "New Description")

        assert result is True
        updated_task = manager.get_task(task.id)
        assert updated_task.title == "New Title"
        assert updated_task.description == "New Description"

    def test_update_nonexistent_task(self):
        """Test that updating a non-existent task returns False."""
        manager = TodoManager()

        result = manager.update_task(999, "New Title", "New Description")

        assert result is False

    def test_mark_task_complete(self):
        """Test that tasks can be marked as complete."""
        manager = TodoManager()
        task = manager.add_task("Test Title", "Test Description")

        result = manager.mark_task_complete(task.id)

        assert result is True
        updated_task = manager.get_task(task.id)
        assert updated_task.completed is True

    def test_mark_task_incomplete(self):
        """Test that tasks can be marked as incomplete."""
        manager = TodoManager()
        task = manager.add_task("Test Title", "Test Description")
        # First mark as complete
        manager.mark_task_complete(task.id)

        result = manager.mark_task_incomplete(task.id)

        assert result is True
        updated_task = manager.get_task(task.id)
        assert updated_task.completed is False

    def test_mark_nonexistent_task_status(self):
        """Test that marking status of non-existent task returns False."""
        manager = TodoManager()

        result = manager.mark_task_complete(999)
        assert result is False

        result = manager.mark_task_incomplete(999)
        assert result is False


if __name__ == "__main__":
    pytest.main([__file__])