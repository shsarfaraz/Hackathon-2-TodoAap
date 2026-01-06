#!/usr/bin/env python3
"""
Test script to verify the CLI enhancements work properly.
This tests the new functionality without requiring interactive input.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from todo_app.todo_manager import TodoManager
from todo_app.models import Task
from datetime import datetime


def test_new_manager_methods():
    """Test the new methods added to TodoManager."""
    print("Testing new TodoManager methods...")

    # Create a manager and add some test tasks
    manager = TodoManager()

    # Add a completed task
    task1 = manager.add_task("Test Task 1", "This is a completed task")
    manager.mark_task_complete(task1.id)

    # Add a pending task
    task2 = manager.add_task("Test Task 2", "This is a pending task")

    # Add another completed task with search term
    task3 = manager.add_task("Searchable Task", "This contains the word important")
    manager.mark_task_complete(task3.id)

    # Test get_tasks_by_status
    completed_tasks = manager.get_tasks_by_status(completed=True)
    pending_tasks = manager.get_tasks_by_status(completed=False)

    print(f"  - Found {len(completed_tasks)} completed tasks")
    print(f"  - Found {len(pending_tasks)} pending tasks")

    assert len(completed_tasks) == 2, f"Expected 2 completed tasks, got {len(completed_tasks)}"
    assert len(pending_tasks) == 1, f"Expected 1 pending task, got {len(pending_tasks)}"

    # Test search_tasks
    search_results = manager.search_tasks("important")
    print(f"  - Found {len(search_results)} tasks matching 'important'")
    assert len(search_results) == 1, f"Expected 1 search result, got {len(search_results)}"
    assert search_results[0].title == "Searchable Task", f"Expected 'Searchable Task', got {search_results[0].title}"

    search_results2 = manager.search_tasks("test")
    print(f"  - Found {len(search_results2)} tasks matching 'test'")
    assert len(search_results2) == 2, f"Expected 2 search results for 'test', got {len(search_results2)}"

    print("  [PASS] All new manager methods work correctly!")


def test_task_model():
    """Test the Task model functionality."""
    print("\nTesting Task model...")

    # Create a task
    task = Task(
        id=1,
        title="Test Task",
        description="This is a test task"
    )

    print(f"  - Created task: {task.title}")
    print(f"  - Task completed: {task.completed}")
    print(f"  - Created at: {task.created_at}")

    # Test mark_complete
    task.mark_complete()
    assert task.completed == True, "Task should be marked as complete"
    print("  - Task marked as complete")

    # Test mark_incomplete
    task.mark_incomplete()
    assert task.completed == False, "Task should be marked as incomplete"
    print("  - Task marked as incomplete")

    # Test update
    original_updated_at = task.updated_at
    task.update(title="Updated Task", description="Updated description")
    assert task.title == "Updated Task", "Task title should be updated"
    assert task.description == "Updated description", "Task description should be updated"
    assert task.updated_at != original_updated_at, "Updated timestamp should change"
    print("  - Task updated successfully")

    print("  [PASS] Task model works correctly!")


def main():
    """Run all tests."""
    print("Running CLI enhancement tests...\n")

    try:
        test_new_manager_methods()
        test_task_model()

        print("\n[PASS] All tests passed! CLI enhancements are working correctly.")
        return True
    except Exception as e:
        print(f"\n[FAIL] Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)