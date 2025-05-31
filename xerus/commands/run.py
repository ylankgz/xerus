import os
import json
from typing import Optional
import rich_click as click

from ..agent import EnhancedAgent
from ..error_handler import handle_command_errors
from ..errors import InputError
from ..sessions import create_session_file, save_session
from ..tools import setup_manager_agent
from ..ui.display import console
from ..ui.progress import create_initialization_progress

@click.command(context_settings={"allow_extra_args": True, "allow_interspersed_args": False})
@click.option("--prompt", required=True, help="[bold]Input prompt[/bold] for the AI model")
@click.option("--save-session", is_flag=True, default=True, help="Save the session to a file")
@click.option("--session-name", help="Name for this session (used in saved session file)")
@click.pass_context
@handle_command_errors
def run(
    ctx,
    prompt, 
    save_session: bool,
    session_name: Optional[str],
):
    """[bold]Run AI model[/bold] configured via config file.

    The manager agent and all tools are configured via ~/.xerus/config.toml

    You can pass additional model parameters as key=value pairs:

    Examples:\n
    [green]xerus run --prompt "Hello"[/green]\n
    [green]xerus run --prompt "Analyze this data" --session-name "analysis"[/green]\n
    [green]xerus run --prompt "Hello" temperature=0.7 top_p=0.95[/green]\n
    [green]xerus run --prompt "Code review" temperature=0.3 max_tokens=1000[/green]\n
    """
    if prompt is None:
        raise InputError("No prompt provided. Please provide a text instruction for the agent to process.")
    
    # Parse additional kwargs from extra arguments
    kwargs = {}
    for arg in ctx.args:
        if "=" in arg:
            key, value = arg.split("=", 1)
            # Try to convert to appropriate type
            try:
                # Try int first
                kwargs[key] = int(value)
            except ValueError:
                try:
                    # Try float
                    kwargs[key] = float(value)
                except ValueError:
                    # Keep as string
                    kwargs[key] = value
        else:
            console.print(f"[yellow]Warning: Ignoring invalid argument format: {arg}[/yellow]")
            console.print("[yellow]Use key=value format for additional parameters[/yellow]")
    
    if kwargs:
        console.print(f"[blue]Using additional parameters: {kwargs}[/blue]")
        
    # Create a progress instance for initialization
    progress = create_initialization_progress()
    
    agent_task = None

    with progress:
        # Add a task for agent initialization
        agent_task = progress.add_task("[bold green]Initializing agent...", total=100)

        # Setup manager agent from config with additional kwargs
        manager_agent = setup_manager_agent(**kwargs)

        # Create the enhanced agent
        enhanced_agent = EnhancedAgent(manager_agent)

        # Mark initialization as complete
        progress.update(agent_task, completed=100)

        response = enhanced_agent.run(prompt)

        # Save session if requested
        if save_session:
            try:
                session_file = create_session_file(session_name)
                save_session(session_file, [
                    {"role": "user", "content": prompt},
                    {"role": "assistant", "content": response}
                ], {})
                console.print(f"[green]Session saved to {session_file}[/green]")
            except Exception as e:
                console.print(f"[yellow]Warning: Could not save session: {str(e)}[/yellow]") 