"""
Main entry point for the Todo Evolution application.

This module initializes and runs the command line interface.
"""

from .cli import TodoCLI


def main():
    """
    Main function to start the Todo Evolution application.

    This function creates and runs the CLI, serving as the entry point
    for the application when executed from the command line.
    """
    # Create and start the CLI application
    cli = TodoCLI()
    cli.start()


if __name__ == "__main__":
    # When this script is run directly, start the application
    main()