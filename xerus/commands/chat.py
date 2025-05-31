import os
import json
from typing import Optional
import rich_click as click

from ..agent import EnhancedAgent
from ..error_handler import handle_command_errors
from ..sessions import (
    create_session_file,
    save_session
)
from ..tools import setup_manager_agent
from ..ui.display import console
from ..ui.progress import create_initialization_progress

@click.command(context_settings={"allow_extra_args": True, "allow_interspersed_args": False})
@click.option("--session-name", help="Name for this session (used in saved session file)")
@click.pass_context
@handle_command_errors
def chat(
    ctx,
    session_name: Optional[str],
):
    """[bold]Interactive chat with AI model[/bold] configured via config file.

    The manager agent and all tools are configured via ~/.xerus/config.toml

    You can pass additional model parameters as key=value pairs:

    Examples:\n
    [green]xerus chat[/green]\n
    [green]xerus chat --session-name "My session"[/green]\n
    [green]xerus chat temperature=0.7 top_p=0.95[/green]\n
    [green]xerus chat --session-name "test" temperature=0.3 max_tokens=1000[/green]\n
    """
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
        agent = EnhancedAgent(manager_agent)

        # Mark initialization as complete
        progress.update(agent_task, completed=100)

    # Create a session file if a name is provided
    session_file = create_session_file(session_name) if session_name else None
    
    # Initialize session history
    session_history = []
    
    console.print("\n[bold blue]Interactive Chat Mode[/bold blue]")
    console.print("[green]Type 'exit', 'quit', or use Ctrl+C to end the session[/green]")
    console.print("[green]Type 'save' to save the current session[/green]\n")

    # Main chat loop
    while True:
        try:
            # Get user input
            user_input = click.prompt("You")
            
            # Check for exit commands
            if user_input.lower() in ["exit", "quit"]:
                console.print("[bold blue]Exiting chat session[/bold blue]")
                # Save session on exit if a name was provided
                if session_name and session_file and session_history:
                    save_session(session_file, session_history, {})
                    console.print(f"[green]Session saved to {session_file}[/green]")
                break
            
            # Check for save command
            if user_input.lower() == "save":
                if not session_history:
                    console.print("[yellow]No conversation to save yet.[/yellow]")
                    continue
                
                save_file = session_file or create_session_file(session_name)
                save_session(save_file, session_history, {})
                console.print(f"[green]Session saved to {save_file}[/green]")
                continue
            
            # Process normal input
            session_history.append({"role": "user", "content": user_input})
            
            # Create a context string from session history
            include_history = len(session_history) > 1
            
            # Run the agent with context and history
            response = agent.run(
                user_input, 
                include_history=include_history,
            )
            
            # Add to session history
            session_history.append({"role": "assistant", "content": response})
                
        except KeyboardInterrupt:
            console.print("\n[bold blue]Chat session interrupted[/bold blue]")
            break
        except Exception as e:
            console.print(f"[bold red]Error during chat: {str(e)}[/bold red]")
            console.print("[green]You can continue chatting or type 'exit' to quit[/green]") 