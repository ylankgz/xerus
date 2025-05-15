"""
Progress reporting utilities for Xerus CLI.
"""
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn, TaskProgressColumn
from rich.console import Console
from typing import Callable, Optional

from .display import console

def create_initialization_progress() -> Progress:
    """Create a progress instance for agent initialization."""
    return Progress(
        SpinnerColumn(),
        TextColumn("[bold green]{task.description}"),
        BarColumn(bar_width=40),
        TaskProgressColumn(),
        TimeElapsedColumn(),
        console=console
    )

def create_execution_progress() -> Progress:
    """Create a progress instance for agent execution."""
    return Progress(
        SpinnerColumn(),
        TextColumn("[cyan]{task.description}"),
        BarColumn(bar_width=40),
        TimeElapsedColumn(),
        console=console
    )

def create_simple_progress() -> Progress:
    """Create a simple progress instance for agent execution."""
    return Progress(
        SpinnerColumn(),
        TextColumn("[cyan]{task.description}"),
        TimeElapsedColumn(),
        console=console
    )

def create_task_progress_callback(progress_instance: Progress, task_id) -> Callable:
    """Create a progress callback function for a specific task."""
    def progress_callback(message, value):
        progress_instance.update(task_id, description=message, completed=int(value * 100) if value is not None else None)
    return progress_callback 