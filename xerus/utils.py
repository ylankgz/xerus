import os
from pathlib import Path
from .ui.display import console

def parse_kwargs(raw_kwargs):
    """Parse key=value arguments into a dictionary"""
    parsed = {}
    for arg in raw_kwargs:
        if "=" not in arg:
            raise ValueError(f"Invalid argument format: {arg}")
        key, value = arg.split("=", 1)
        parsed[key] = value
    return parsed

def is_xerus_initialized() -> bool:
    """Check if xerus is properly initialized with both config.json and .env files"""
    xerus_dir = Path.home() / '.xerus'
    config_file = xerus_dir / 'config.json'
    env_file = xerus_dir / '.env'
    return config_file.exists() and env_file.exists()

def show_initialization_message():
    """Show message when xerus is not initialized"""
    console.print("[bold red]Xerus is not initialized![/bold red]")
    console.print("[yellow]Please run the following command to initialize Xerus:[/yellow]")
    console.print("[green]xerus init[/green]")
    console.print("\n[blue]This will set up your configuration with an AI provider.[/blue]") 