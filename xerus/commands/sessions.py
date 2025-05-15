import os
import json
from pathlib import Path
import rich_click as click
from rich.markdown import Markdown

from ..sessions import get_session_dir, load_session
from ..ui.display import console
from ..error_handler import handle_command_errors

@click.command("sessions")
@handle_command_errors
def list_sessions_command():
    """List all saved sessions."""
    session_dir = get_session_dir()
    sessions = list(session_dir.glob("*.json"))
    
    if not sessions:
        console.print("[yellow]No saved sessions found.[/yellow]")
        return
    
    console.print("[bold blue]Saved Sessions:[/bold blue]")
    for idx, session_file in enumerate(sorted(sessions, key=lambda x: x.stat().st_mtime, reverse=True)):
        try:
            with open(session_file, "r") as f:
                data = json.load(f)
            
            # Get metadata if available
            metadata = data.get("metadata", {})
            model_info = f"{metadata.get('model_type', 'unknown')}/{metadata.get('model_id', 'unknown')}"
            timestamp = metadata.get("timestamp") or data.get("timestamp", "unknown time")
            
            # Get message count
            history = data.get("history", [])
            message_count = len(history)
            
            # Display session info
            console.print(f"{idx+1}. [bold]{session_file.name}[/bold]")
            console.print(f"   [dim]Created: {timestamp}[/dim]")
            console.print(f"   [dim]Model: {model_info}[/dim]")
            console.print(f"   [dim]Messages: {message_count}[/dim]")
            
            # Show first exchange if available
            if history and len(history) >= 2:
                first_prompt = history[0].get("content", "")
                console.print(f"   [dim]First prompt: {first_prompt[:50]}{'...' if len(first_prompt) > 50 else ''}[/dim]")
            
            console.print()
            
        except Exception as e:
            console.print(f"[yellow]Error reading {session_file.name}: {str(e)}[/yellow]")

@click.command("load")
@click.option("--session", "-s", help="Name or path of the session file to load")
@click.option("--format", "-f", default="rich", type=click.Choice(["rich", "plain", "json", "markdown"]), help="Output format")
@handle_command_errors
def load_session_command(session, format="rich"):
    """Load and display a saved session."""
    # Check if session is None
    if session is None:
        console.print("[red]Error: No session file specified. Please provide a session file name or path.[/red]")
        return
        
    # Resolve the session file path
    session_dir = get_session_dir()
    session_path = None
    
    # If just a name was provided, find it in the sessions directory
    if not os.path.isfile(session):
        # Try exact match
        potential_path = session_dir / session
        if potential_path.exists():
            session_path = potential_path
        else:
            # Try adding .json extension
            potential_path = session_dir / f"{session}.json"
            if potential_path.exists():
                session_path = potential_path
            else:
                # Look for partial matches
                matches = list(session_dir.glob(f"*{session}*.json"))
                if len(matches) == 1:
                    session_path = matches[0]
                elif len(matches) > 1:
                    console.print("[yellow]Multiple matching sessions found:[/yellow]")
                    for match in matches:
                        console.print(f"  {match.name}")
                    console.print("[yellow]Please specify a more precise name.[/yellow]")
                    return
    else:
        # If a full path was provided
        session_path = Path(session)
    
    if not session_path or not session_path.exists():
        console.print(f"[red]Session file '{session}' not found.[/red]")
        return
    
    # Load the session
    console.print(f"[green]Loading session from {session_path}[/green]")
    session_data = load_session(session_path)
    
    # Display the conversation
    history = session_data.get("history", [])
    metadata = session_data.get("metadata", {})
    
    # Show metadata if available
    if metadata:
        console.print("[bold blue]Session Info:[/bold blue]")
        for key, value in metadata.items():
            console.print(f"[bold]{key}:[/bold] {value}")
        console.print()
    
    console.print("[bold blue]Conversation:[/bold blue]")
    for entry in history:
        role = entry.get("role", "unknown")
        content = entry.get("content", "")
        
        if role == "user":
            console.print("\n[bold cyan]You:[/bold cyan]")
            console.print(content)
        elif role == "assistant":
            console.print("\n[bold green]Agent:[/bold green]")
            if format == "rich":
                console.print(Markdown(content))
            elif format == "plain":
                console.print(content)
            elif format == "json":
                console.print(json.dumps({"response": content}, indent=2))
            elif format == "markdown":
                console.print(Markdown(content)) 