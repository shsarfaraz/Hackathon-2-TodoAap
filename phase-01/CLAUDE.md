# Claude Code Instructions for Todo Evolution Project

This document provides instructions on how to use Claude Code with the Todo Evolution project, following spec-driven development principles.

## Project Overview

The Todo Evolution - Phase I project is a simple CLI todo application that stores tasks in memory. It demonstrates spec-driven development using Claude Code and Spec-Kit Plus.

## Claude Code Setup

### Prerequisites
- Claude Code CLI installed
- Python 3.13+ environment
- UV package manager

### Initial Setup
1. Navigate to your project directory
2. Initialize Claude Code if not already done:
   ```bash
   claude-code init
   ```

## Spec-Driven Development Workflow

### 1. Creating New Features

To create a new feature using Claude Code:

1. **Use the `/sp.specify` command**:
   ```
   /sp.specify
   Project: [Feature Name]
   Focus: [Feature Focus]
   Goal: [Feature Goal]
   Requirements: [List requirements]
   ```

2. **Claude Code will**:
   - Generate a unique branch name
   - Create specification files in `specs_history/`
   - Initialize source code files based on the spec

### 2. Available Claude Code Commands

#### Specification Commands
- `/sp.specify` - Create new feature specifications
- `/sp.plan` - Generate implementation plan
- `/sp.tasks` - Generate development tasks
- `/sp.clarify` - Clarify specification details

#### Development Commands
- `/sp.implement` - Execute implementation plan
- `/sp.analyze` - Analyze code quality and consistency
- `/sp.adr` - Create architectural decision records
- `/sp.phr` - Create prompt history records

#### Project Management Commands
- `/sp.constitution` - Update project constitution
- `/sp.checklist` - Generate custom checklists
- `/sp.git.commit_pr` - Create commits and PRs

### 3. Working with the Todo App

#### Adding New Functionality
1. Create a specification using `/sp.specify`
2. Review the generated spec in `specs_history/spec.md`
3. Use `/sp.plan` to generate implementation plan
4. Use `/sp.tasks` to generate specific tasks
5. Implement using the existing code structure in `src/todo_app/`

#### Example: Adding a Search Feature
```
/sp.specify
Project: "Todo Evolution - Phase I"
Focus: Add task search functionality
Goal: Allow users to search for tasks by title or description
Requirements:
1. Implement search by title
2. Implement search by description
3. Display search results with pagination
4. Case-insensitive search
```

### 4. Code Structure and Conventions

#### Project Structure
```
todo-evolution/
├── .specify/                 # Claude Code configuration
│   ├── memory/              # Project constitution
│   └── templates/           # Spec templates
├── specs_history/           # Feature specifications
├── src/                     # Source code
│   └── todo_app/            # Main package
│       ├── __init__.py      # Package init
│       ├── main.py          # Entry point
│       ├── models.py        # Data models
│       ├── todo_manager.py  # Business logic
│       └── cli.py           # User interface
```

#### Code Conventions
- Follow PEP 8 style guidelines
- Include comprehensive docstrings
- Use type hints for all functions
- Write clear, descriptive comments
- Follow the existing architecture patterns

### 5. Best Practices with Claude Code

#### Specification Quality
- Write clear, testable requirements
- Define success criteria quantitatively
- Consider edge cases and error handling
- Keep specifications focused and achievable

#### Implementation Guidelines
- Follow the principle of simplicity-first
- Maintain in-memory persistence approach
- Keep the console interface user-friendly
- Ensure all operations complete efficiently

#### Testing Approach
- Write unit tests for all new functionality
- Test edge cases and error conditions
- Verify user interface flows
- Maintain performance standards

### 6. Troubleshooting Common Issues

#### Issue: Specification not generating properly
**Solution**: Ensure requirements are specific and testable
```
# Instead of: "Make it work better"
# Use: "Improve search performance to return results in under 100ms"
```

#### Issue: Code conflicts during generation
**Solution**: Review generated code before accepting, make manual adjustments if needed

#### Issue: Dependency problems
**Solution**: Use UV package manager as specified in project requirements

### 7. Development Workflow Example

1. **Start a new feature**:
   ```
   /sp.specify
   Project: "Todo Evolution - Export Feature"
   Focus: Export tasks to JSON
   Goal: Allow users to export their tasks to a JSON file
   Requirements:
   1. Add export option to main menu
   2. Export all tasks to JSON format
   3. Save to user-specified file path
   ```

2. **Review generated specification** in `specs_history/spec.md`

3. **Generate implementation plan**:
   ```
   /sp.plan
   ```

4. **Generate tasks**:
   ```
   /sp.tasks
   ```

5. **Implement using existing patterns** from `src/todo_app/`

6. **Create implementation**:
   ```
   /sp.implement
   ```

### 8. Quality Assurance

When using Claude Code for this project, ensure:

- All generated code follows the existing architecture
- Specifications align with project constitution
- New features maintain simplicity and usability
- Performance requirements are met
- Error handling is comprehensive

### 9. Resources

- [Claude Code Documentation](https://docs.anthropic.com/claude-code)
- [Spec-Kit Plus Guide](https://spec-kit-plus.example.com)
- [Python 3.13 Documentation](https://docs.python.org/3.13/)
- [UV Package Manager](https://github.com/astral-sh/uv)

### 10. Getting Help

For questions about using Claude Code with this project:
- Check the Claude Code documentation first
- Review existing specifications in `specs_history/`
- Examine the implementation patterns in `src/todo_app/`
- Use `/sp.clarify` for specification questions