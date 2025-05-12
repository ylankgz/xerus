"""
CLI module for Xerus package.

This package contains the command-line interface for Xerus.
It is organized into separate modules for better maintainability:

- app: Main Typer application and command definitions
- commands: Implementations of CLI commands
- sessions: Session management utilities
- progress: Progress reporting utilities
"""

from .app import app, cli, run 