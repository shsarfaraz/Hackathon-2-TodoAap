# Todo Evolution - Phase I

A simple, in-memory console-based todo application built with Python. This application allows users to manage their tasks through a command-line interface with all data stored in memory during the session.

## Features

- **Add Tasks**: Create new tasks with titles and descriptions
- **View Tasks**: Display all tasks with clear status indicators
- **Update Tasks**: Modify existing task details
- **Delete Tasks**: Remove tasks by ID
- **Mark Complete/Incomplete**: Track task completion status
- **User-Friendly Interface**: Intuitive menu-driven console interface

## Prerequisites

- Python 3.13 or higher
- UV package manager (recommended) or pip

## Installation

### Using UV (Recommended)

1. **Install UV** (if not already installed):
   ```bash
   pip install uv
   ```

2. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd todo-evolution
   ```

3. **Install dependencies**:
   ```bash
   uv sync
   ```

4. **Run the application**:
   ```bash
   uv run python -m src.todo_app
   ```

### Using Pip

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd todo-evolution
   ```

2. **Create and activate virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -e .
   ```

4. **Run the application**:
   ```bash
   python -m src.todo_app
   ```

## Usage

Once the application starts, you'll see a menu with the following options:

1. **Add Task**: Create a new task by providing a title and description
2. **View All Tasks**: Display all tasks with their status (complete/incomplete)
3. **Update Task**: Modify an existing task's title or description
4. **Delete Task**: Remove a task by its ID
5. **Mark Task Complete**: Mark a task as completed
6. **Mark Task Incomplete**: Mark a completed task as pending
7. **Exit**: Quit the application

### Example Workflow

1. Start the application
2. Choose "1. Add Task" to create a new task
3. Enter a title (e.g., "Buy groceries") and description (e.g., "Milk, bread, eggs")
4. Choose "2. View All Tasks" to see your task
5. Choose "5. Mark Task Complete" to mark it as done
6. Continue managing your tasks as needed

## Project Structure

```
todo-evolution/
├── .specify/                 # Spec-Kit Plus configuration
│   ├── memory/              # Project constitution
│   └── templates/           # Specification templates
├── specs_history/           # Project specifications
├── src/                     # Source code
│   └── todo_app/            # Main application package
│       ├── __init__.py      # Package initialization
│       ├── main.py          # Application entry point
│       ├── models.py        # Data models (Task class)
│       ├── todo_manager.py  # Core business logic
│       └── cli.py           # Command line interface
├── tests/                   # Test files
└── docs/                    # Documentation
```

## Development

### Running Tests

```bash
# Using UV
uv run pytest

# Using pip
python -m pytest
```

### Code Style

This project follows PEP 8 guidelines for Python code style. All functions and classes include docstrings following the Google Python Style Guide.

## Limitations

- **In-Memory Storage**: All tasks are stored in memory and will be lost when the application closes
- **Single User**: The application supports only one user session at a time
- **No Persistence**: Tasks are not saved to disk or database

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests if applicable
5. Run tests to ensure everything works (`uv run pytest`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with Python 3.13+
- Uses UV package manager for dependency management
- Follows spec-driven development principles with Claude Code and Spec-Kit Plus