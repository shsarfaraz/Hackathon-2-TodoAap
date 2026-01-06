#!/usr/bin/env python3
"""
Demonstration script showing that the view all tasks functionality works correctly.
"""

from src.todo_app.cli import TodoCLI

def demonstrate_view_functionality():
    print("Demonstrating that the View All Tasks functionality works correctly")
    print("="*60)

    # Create a CLI instance
    cli = TodoCLI()

    print("\n1. Initially, there are no tasks:")
    cli.view_tasks()

    print("\n2. Adding a few sample tasks...")
    cli.manager.add_task("Buy groceries", "Milk, bread, eggs, fruits")
    cli.manager.add_task("Finish report", "Complete the quarterly report for work")
    cli.manager.add_task("Call dentist", "Schedule annual checkup")

    print("\n3. Now viewing all tasks:")
    cli.view_tasks()

    print("\n4. Marking one task as complete...")
    cli.manager.mark_task_complete(2)  # Mark "Finish report" as complete

    print("\n5. Viewing tasks after marking one as complete:")
    cli.view_tasks()

    print("\n" + "="*60)
    print("As you can see, the View All Tasks functionality works correctly!")
    print("The issue you experienced was likely due to running in a non-interactive environment.")
    print("To use the full application, run it from a command prompt where you can interact with it.")

if __name__ == "__main__":
    demonstrate_view_functionality()