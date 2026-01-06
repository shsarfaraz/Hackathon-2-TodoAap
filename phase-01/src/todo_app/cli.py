"""
Command Line Interface for the Todo Evolution application.

This module handles user interaction through the console,
providing menus and input processing for all todo operations.
"""

import json
from typing import Optional
from .todo_manager import TodoManager


class TodoCLI:
    """
    Command Line Interface for the Todo application.

    This class manages the user interface, displaying menus,
    processing user input, and coordinating with the TodoManager.
    """

    def __init__(self):
        """Initialize the CLI with a TodoManager instance."""
        self.manager = TodoManager()
        self.running = True

    def display_menu(self) -> None:
        """Display the main menu options to the user."""
        print("\n" + "="*50)
        print("           TODO EVOLUTION - PHASE I")
        print("="*50)
        print("1. Add Task")
        print("2. View All Tasks")
        print("3. View Tasks by Status")
        print("4. Search Tasks")
        print("5. Update Task")
        print("6. Delete Task")
        print("7. Mark Task Complete")
        print("8. Mark Task Incomplete")
        print("9. Export Tasks")
        print("10. Exit")
        print("="*50)

    def get_user_choice(self) -> str:
        """
        Get and validate user menu choice.

        Returns:
            The user's menu choice as a string
        """
        while True:
            choice = input("Enter your choice (1-10): ").strip()
            if choice in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']:
                return choice
            else:
                print("Invalid choice. Please enter a number between 1 and 10.")

    def add_task(self) -> None:
        """Handle the add task operation."""
        print("\n--- Add New Task ---")
        title = input("Enter task title: ").strip()

        # Validate title
        if not title:
            print("Error: Task title cannot be empty.")
            return

        description = input("Enter task description: ").strip()

        # Create the task
        task = self.manager.add_task(title, description)
        print(f"✓ Task added successfully! ID: {task.id}")

    def view_tasks(self) -> None:
        """Handle the view all tasks operation."""
        print("\n--- All Tasks ---")
        tasks = self.manager.get_all_tasks()

        if not tasks:
            print("No tasks found. Your todo list is empty!")
            return

        # Display all tasks with status indicators
        for task in tasks:
            status_indicator = "X" if task.completed else " "
            completion_text = "COMPLETED" if task.completed else "PENDING"
            print(f"[{status_indicator}] ID: {task.id} | {task.title}")
            print(f"    Description: {task.description}")
            print(f"    Status: {completion_text}")
            print("-" * 40)

    def view_tasks_by_status(self) -> None:
        """Handle the view tasks by status operation."""
        print("\n--- View Tasks by Status ---")
        print("1. View Completed Tasks")
        print("2. View Pending Tasks")

        while True:
            status_choice = input("Enter your choice (1-2): ").strip()
            if status_choice in ['1', '2']:
                break
            else:
                print("Invalid choice. Please enter 1 or 2.")

        if status_choice == '1':
            filtered_tasks = self.manager.get_tasks_by_status(completed=True)
            status_name = "COMPLETED"
        else:
            filtered_tasks = self.manager.get_tasks_by_status(completed=False)
            status_name = "PENDING"

        if not filtered_tasks:
            print(f"No {status_name.lower()} tasks found!")
            return

        print(f"\n--- {status_name} Tasks ---")
        for task in filtered_tasks:
            status_indicator = "X" if task.completed else " "
            print(f"[{status_indicator}] ID: {task.id} | {task.title}")
            print(f"    Description: {task.description}")
            print("-" * 40)

    def search_tasks(self) -> None:
        """Handle the search tasks operation."""
        print("\n--- Search Tasks ---")
        query = input("Enter search term: ").strip()

        if not query:
            print("Search term cannot be empty.")
            return

        matching_tasks = self.manager.search_tasks(query)

        if not matching_tasks:
            print("No tasks found matching your search.")
            return

        print(f"\n--- Search Results for '{query}' ---")
        for task in matching_tasks:
            status_indicator = "X" if task.completed else " "
            completion_text = "COMPLETED" if task.completed else "PENDING"
            print(f"[{status_indicator}] ID: {task.id} | {task.title}")
            print(f"    Description: {task.description}")
            print(f"    Status: {completion_text}")
            print("-" * 40)

    def update_task(self) -> None:
        """Handle the update task operation."""
        print("\n--- Update Task ---")

        # Get task ID from user
        task_id_str = input("Enter task ID to update: ").strip()
        try:
            task_id = int(task_id_str)
        except ValueError:
            print("Error: Task ID must be a number.")
            return

        # Check if task exists
        task = self.manager.get_task(task_id)
        if not task:
            print(f"Error: Task with ID {task_id} not found.")
            return

        # Show current task details
        print(f"Current task: {task.title}")
        print(f"Current description: {task.description}")

        # Get new title (or keep current if empty)
        new_title = input(f"Enter new title (leave blank to keep '{task.title}'): ").strip()
        if not new_title:
            new_title = task.title

        # Get new description (or keep current if empty)
        new_description = input(f"Enter new description (leave blank to keep current): ").strip()
        if not new_description:
            new_description = task.description

        # Update the task
        if self.manager.update_task(task_id, new_title, new_description):
            print(f"✓ Task {task_id} updated successfully!")
        else:
            print(f"Error: Failed to update task {task_id}")

    def delete_task(self) -> None:
        """Handle the delete task operation."""
        print("\n--- Delete Task ---")

        # Get task ID from user
        task_id_str = input("Enter task ID to delete: ").strip()
        try:
            task_id = int(task_id_str)
        except ValueError:
            print("Error: Task ID must be a number.")
            return

        # Confirm deletion
        task = self.manager.get_task(task_id)
        if not task:
            print(f"Error: Task with ID {task_id} not found.")
            return

        print(f"Task to delete: {task.title}")
        confirm = input("Are you sure you want to delete this task? (y/N): ").strip().lower()

        if confirm == 'y':
            if self.manager.delete_task(task_id):
                print(f"✓ Task {task_id} deleted successfully!")
            else:
                print(f"Error: Failed to delete task {task_id}")
        else:
            print("Deletion cancelled.")

    def export_tasks(self) -> None:
        """Handle the export tasks operation."""
        print("\n--- Export Tasks ---")
        tasks = self.manager.get_all_tasks()

        if not tasks:
            print("No tasks to export.")
            return

        filename = input("Enter filename to export to (default: tasks.json): ").strip()
        if not filename:
            filename = "tasks.json"

        # Convert tasks to dictionary format for JSON serialization
        tasks_data = []
        for task in tasks:
            task_dict = {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "created_at": task.created_at.isoformat() if task.created_at else None,
                "updated_at": task.updated_at.isoformat() if task.updated_at else None
            }
            tasks_data.append(task_dict)

        try:
            with open(filename, 'w') as f:
                json.dump(tasks_data, f, indent=2)
            print(f"✓ Tasks exported successfully to {filename}!")
        except Exception as e:
            print(f"Error exporting tasks: {e}")

    def mark_task_complete(self) -> None:
        """Handle marking a task as complete."""
        print("\n--- Mark Task Complete ---")
        self._mark_task_status(True)

    def mark_task_incomplete(self) -> None:
        """Handle marking a task as incomplete."""
        print("\n--- Mark Task Incomplete ---")
        self._mark_task_status(False)

    def _mark_task_status(self, complete: bool) -> None:
        """
        Helper method to mark a task's completion status.

        Args:
            complete: True to mark complete, False to mark incomplete
        """
        # Get task ID from user
        task_id_str = input("Enter task ID: ").strip()
        try:
            task_id = int(task_id_str)
        except ValueError:
            print("Error: Task ID must be a number.")
            return

        # Check if task exists
        task = self.manager.get_task(task_id)
        if not task:
            print(f"Error: Task with ID {task_id} not found.")
            return

        # Update task status
        if complete:
            if self.manager.mark_task_complete(task_id):
                print(f"✓ Task {task_id} marked as complete!")
            else:
                print(f"Error: Failed to mark task {task_id} as complete")
        else:
            if self.manager.mark_task_incomplete(task_id):
                print(f"✓ Task {task_id} marked as incomplete!")
            else:
                print(f"Error: Failed to mark task {task_id} as incomplete")

    def run(self) -> None:
        """Run the main application loop."""
        print("Welcome to Todo Evolution - Phase I!")
        print("A simple in-memory console todo application.")

        while self.running:
            self.display_menu()
            choice = self.get_user_choice()

            if choice == '1':
                self.add_task()
            elif choice == '2':
                self.view_tasks()
            elif choice == '3':
                self.view_tasks_by_status()
            elif choice == '4':
                self.search_tasks()
            elif choice == '5':
                self.update_task()
            elif choice == '6':
                self.delete_task()
            elif choice == '7':
                self.mark_task_complete()
            elif choice == '8':
                self.mark_task_incomplete()
            elif choice == '9':
                self.export_tasks()
            elif choice == '10':
                print("\nThank you for using Todo Evolution!")
                print("Your tasks will be lost when the application closes.")
                self.running = False

    def start(self) -> None:
        """Start the CLI application."""
        try:
            self.run()
        except KeyboardInterrupt:
            print("\n\nApplication interrupted by user.")
            print("Goodbye!")
        except Exception as e:
            print(f"\nAn unexpected error occurred: {e}")
            print("Please restart the application.")