import sys
import rich_click as click
from pathlib import Path

from . import __version__
from .ui.display import print_welcome, print_project_info

# Configure rich-click
click.rich_click.USE_RICH_MARKUP = True
click.rich_click.STYLE_HELPTEXT = "cyan"
click.rich_click.STYLE_OPTION = "bold green"
click.rich_click.STYLE_COMMAND = "bold yellow"

# Try to load environment variables from .env file if python-dotenv is installed
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # Not raising an error since dotenv is optional
    import warnings
    warnings.warn(
        "python-dotenv package not installed. Environment variables from .env files will not be loaded. "
        "Install with: pip install python-dotenv"
    )

@click.group(invoke_without_command=True)
@click.version_option(__version__, prog_name="Xerus")
@click.pass_context
def main(ctx):
    """[bold]Xerus - CLI Agent for creating and managing ML models[/bold] :chipmunk:"""
    if ctx.invoked_subcommand is None:
        print_welcome()
        print_project_info()

# Import and register commands
from .commands.run import run
from .commands.chat import chat
from .commands.sessions import list_sessions_command, load_session_command

# Add commands to the CLI
main.add_command(run, name="run")
main.add_command(chat, name="chat")
main.add_command(list_sessions_command, name="sessions")
main.add_command(load_session_command, name="load")

if __name__ == "__main__":
    main() 
