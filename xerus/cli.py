"""
CLI module for Xerus package.
"""
import os
import sys
import json
import typer
from typing import List, Optional, Dict, Any, Callable
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn, TaskProgressColumn
from rich.markdown import Markdown
from pathlib import Path
from datetime import datetime

from . import __version__
from .agent import create_agent, EnhancedAgent
from .display import (
    console, print_welcome, print_project_info, print_prompt_panel,
    print_response_panel, print_error_panel, print_auth_error,
    print_formatted_response
)
from .errors import (
    XerusError, ModelInitializationError, AuthenticationError,
    ToolLoadError, ToolExecutionError, ModelNotFoundError,
    ModelConfigurationError, AgentRuntimeError, NetworkError,
    APILimitError, EnvironmentError, InputError
)

app = typer.Typer(add_completion=False)

def get_history_file_path() -> Path:
    """Get the path to the conversation history file."""
    xerus_dir = Path.home() / ".xerus"
    xerus_dir.mkdir(exist_ok=True)
    return xerus_dir / "history.json"

def get_session_dir() -> Path:
    """Get the directory for session data."""
    xerus_dir = Path.home() / ".xerus" / "sessions"
    xerus_dir.mkdir(exist_ok=True, parents=True)
    return xerus_dir

def create_session_file(name=None) -> Path:
    """Create a new session file with optional name."""
    session_dir = get_session_dir()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    name_part = f"_{name}" if name else ""
    session_file = session_dir / f"session{name_part}_{timestamp}.json"
    return session_file

def load_conversation_history() -> List[Dict[str, Any]]:
    """Load conversation history from file."""
    history_file = get_history_file_path()
    if history_file.exists():
        try:
            with open(history_file, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            console.print("[yellow]Warning: Could not parse history file. Starting with empty history.[/yellow]")
    return []

def save_conversation_history(history: List[Dict[str, Any]]):
    """Save conversation history to file."""
    history_file = get_history_file_path()
    # Limit history to last 50 exchanges to prevent file from growing too large
    history_to_save = history[-50:] if len(history) > 50 else history
    with open(history_file, "w") as f:
        json.dump(history_to_save, f)

def save_session(session_file: Path, history: List[Dict[str, Any]], metadata: Dict[str, Any] = None):
    """Save session to a file."""
    data = {
        "history": history,
        "timestamp": datetime.now().isoformat(),
        "metadata": metadata or {}
    }
    with open(session_file, "w") as f:
        json.dump(data, f, indent=2)
    return session_file

def load_session(session_file: Path) -> Dict[str, Any]:
    """Load a session from a file."""
    with open(session_file, "r") as f:
        return json.load(f)

@app.callback(invoke_without_command=True)
def callback(
    ctx: typer.Context,
    model_type: Optional[str] = typer.Option(
        None, 
        help="Type of model to use: inference (Hugging Face), openai, azure-openai, amazon-bedrock, litellm, transformers, or mlx-lm"
    ),
    model_id: Optional[str] = typer.Option(
        None,
        help="Model identifier (e.g., 'Qwen/Qwen2.5-Coder-32B-Instruct', 'gpt-4', 'mistralai/Mistral-7B-Instruct-v0.1')"
    ),
    api_key: Optional[str] = typer.Option(
        None, 
        help="API key for the model service (can also use environment variables like OPENAI_API_KEY)"
    ),
    tools: Optional[str] = typer.Option(
        None,
        help="Comma-separated list of tools to enable (e.g., 'web_search,path/to/tool.py,hub:user/tool')"
    ),
    imports: Optional[str] = typer.Option(
        None,
        help="Space-separated list of Python packages that the agent is authorized to import (e.g., 'numpy matplotlib pandas')"
    ),
    tool_local: Optional[str] = typer.Option(
        None,
        help="Path to a local tool file"
    ),
    tool_hub: Optional[str] = typer.Option(
        None,
        help="Hugging Face Hub repo ID for a tool"
    ),
    tool_space: Optional[str] = typer.Option(
        None,
        help="Hugging Face Space ID to import as a tool (format: space_id:name:description)"
    ),
    tool_collection: Optional[str] = typer.Option(
        None,
        help="Hugging Face Hub repo ID for a collection of tools"
    ),
    tool_dirs: Optional[str] = typer.Option(
        None,
        help="Comma-separated list of directories to discover tools from"
    )
):
    """Xerus CLI - An AI agent powered by Huggingface Smolagents"""
    print_welcome()
    
    # If no subcommand is provided, show project info
    if ctx.invoked_subcommand is None:
        print_project_info()

@app.command(name="run")
def run(
    prompt: str = typer.Argument(..., help="Text instruction for the agent to process"),
    model_type: str = typer.Option(
        "inference", 
        help="Type of model to use: inference (Hugging Face), openai, azure-openai, amazon-bedrock, litellm, transformers, or mlx-lm"
    ),
    model_id: str = typer.Option(
        "Qwen/Qwen2.5-Coder-32B-Instruct",
        help="Model identifier (e.g., 'Qwen/Qwen2.5-Coder-32B-Instruct', 'gpt-4', 'mistralai/Mistral-7B-Instruct-v0.1')"
    ),
    api_key: Optional[str] = typer.Option(
        None, 
        help="API key for the model service (can also use environment variables like OPENAI_API_KEY)"
    ),
    tools: Optional[str] = typer.Option(
        None,
        help="Comma-separated list of tools to enable (e.g., 'web_search,path/to/tool.py,hub:user/tool')"
    ),
    imports: Optional[str] = typer.Option(
        None,
        help="Space-separated list of Python packages that the agent is authorized to import (e.g., 'numpy matplotlib pandas')"
    ),
    tool_local: Optional[str] = typer.Option(
        None,
        help="Path to a local tool file"
    ),
    tool_hub: Optional[str] = typer.Option(
        None,
        help="Hugging Face Hub repo ID for a tool"
    ),
    tool_space: Optional[str] = typer.Option(
        None,
        help="Hugging Face Space ID to import as a tool (format: space_id:name:description)"
    ),
    tool_collection: Optional[str] = typer.Option(
        None,
        help="Hugging Face Hub repo ID for a collection of tools"
    ),
    tool_dirs: Optional[str] = typer.Option(
        None,
        help="Comma-separated list of directories to discover tools from"
    ),
    output_format: str = typer.Option(
        "rich", 
        help="Output format (rich, plain, json, markdown)"
    ),
    save_session: bool = typer.Option(
        False,
        help="Save this session to a file for later reference"
    )
):
    """Run the agent with a prompt."""
    try:
        # Create a progress instance for initialization
        progress = Progress(
            SpinnerColumn(),
            TextColumn("[bold green]{task.description}"),
            BarColumn(bar_width=40),
            TaskProgressColumn(),
            TimeElapsedColumn(),
            console=console
        )
        
        agent_task = None
        
        # Progress callback function
        def progress_callback(message, value):
            nonlocal agent_task
            if agent_task is not None:
                progress.update(agent_task, description=message, completed=int(value * 100))
        
        with progress:
            # Add a task for agent initialization
            agent_task = progress.add_task("[bold green]Initializing agent...", total=100)
            
            # Setup tools
            tool_list = tools.split(",") if tools else []
            tool_directories = tool_dirs.split(",") if tool_dirs else None
            
            # Create the agent with progress reporting
            base_agent = create_agent(
                model_type, model_id, api_key, tool_list, imports, 
                tool_local, tool_hub, tool_space, tool_collection,
                tool_directories, progress_callback=progress_callback
            )
            
            # Create the enhanced agent
            agent = EnhancedAgent(base_agent)
            
            # Mark initialization as complete
            progress.update(agent_task, completed=100)
        
        print_prompt_panel(prompt)
        
        # Create a new progress for the agent execution
        with Progress(
            SpinnerColumn(),
            TextColumn("[cyan]{task.description}"),
            BarColumn(bar_width=40),
            TimeElapsedColumn(),
            console=console
        ) as run_progress:
            run_task = run_progress.add_task("[cyan]Processing query...", total=None)
            
            # Run the agent
            response = agent.run(prompt, progress_callback=lambda msg, val: 
                                run_progress.update(run_task, description=f"[cyan]{msg}"))
            
            # Mark task as completed
            run_progress.update(run_task, completed=True, total=1.0, description="[green]Response ready")
        
        # Display response in the requested format
        print_formatted_response(response, output_format)
        
        # Save session if requested
        if save_session:
            session_file = create_session_file()
            save_session(session_file, [
                {"role": "user", "content": prompt},
                {"role": "assistant", "content": response}
            ], {
                "model_type": model_type,
                "model_id": model_id,
                "output_format": output_format
            })
            console.print(f"[green]Session saved to {session_file}[/green]")
    
    except AuthenticationError as e:
        print_auth_error(str(e), e.recovery_hint)
        sys.exit(1)
    except ModelNotFoundError as e:
        print_error_panel("Model Not Found", str(e), "Model Error", e.recovery_hint)
        sys.exit(1)
    except ModelInitializationError as e:
        print_error_panel("Model Error", str(e), "Model Initialization Failed", e.recovery_hint)
        sys.exit(1)
    except ModelConfigurationError as e:
        print_error_panel("Configuration Error", str(e), "Model Configuration Error", e.recovery_hint)
        sys.exit(1)
    except ToolLoadError as e:
        print_error_panel("Tool Error", str(e), "Tool Loading Failed", e.recovery_hint)
        sys.exit(1)
    except ToolExecutionError as e:
        print_error_panel("Tool Error", str(e), "Tool Execution Failed", e.recovery_hint)
        sys.exit(1)
    except NetworkError as e:
        print_error_panel("Network Error", str(e), "Connection Failed", e.recovery_hint)
        sys.exit(1)
    except APILimitError as e:
        print_error_panel("API Limit Error", str(e), "API Limit Reached", e.recovery_hint)
        sys.exit(1)
    except AgentRuntimeError as e:
        print_error_panel("Agent Error", str(e), "Execution Failed", e.recovery_hint)
        sys.exit(1)
    except EnvironmentError as e:
        print_error_panel("Environment Error", str(e), "Environment Setup Failed", e.recovery_hint)
        sys.exit(1)
    except InputError as e:
        print_error_panel("Input Error", str(e), "Invalid Input", e.recovery_hint)
        sys.exit(1)
    except XerusError as e:
        print_error_panel("Xerus Error", str(e), "Error", e.recovery_hint)
        sys.exit(1)
    except Exception as e:
        print_error_panel("Unexpected Error", str(e), "Unhandled Error", 
                         "Please report this issue to the Xerus developers")
        sys.exit(1)

@app.command(name="chat")
def chat(
    model_type: str = typer.Option(
        "inference", 
        help="Type of model to use: inference (Hugging Face), openai, azure-openai, amazon-bedrock, litellm, transformers, or mlx-lm"
    ),
    model_id: str = typer.Option(
        "Qwen/Qwen2.5-Coder-32B-Instruct",
        help="Model identifier (e.g., 'Qwen/Qwen2.5-Coder-32B-Instruct', 'gpt-4', 'mistralai/Mistral-7B-Instruct-v0.1')"
    ),
    api_key: Optional[str] = typer.Option(
        None, 
        help="API key for the model service (can also use environment variables like OPENAI_API_KEY)"
    ),
    tools: Optional[str] = typer.Option(
        None,
        help="Comma-separated list of tools to enable (e.g., 'web_search,path/to/tool.py,hub:user/tool')"
    ),
    imports: Optional[str] = typer.Option(
        None,
        help="Space-separated list of Python packages that the agent is authorized to import (e.g., 'numpy matplotlib pandas')"
    ),
    tool_local: Optional[str] = typer.Option(
        None,
        help="Path to a local tool file"
    ),
    tool_hub: Optional[str] = typer.Option(
        None,
        help="Hugging Face Hub repo ID for a tool"
    ),
    tool_space: Optional[str] = typer.Option(
        None,
        help="Hugging Face Space ID to import as a tool (format: space_id:name:description)"
    ),
    tool_collection: Optional[str] = typer.Option(
        None,
        help="Hugging Face Hub repo ID for a collection of tools"
    ),
    tool_dirs: Optional[str] = typer.Option(
        None,
        help="Comma-separated list of directories to discover tools from"
    ),
    output_format: str = typer.Option(
        "rich", 
        help="Output format (rich, plain, json, markdown)"
    ),
    no_history: bool = typer.Option(
        False,
        help="Don't load or save conversation history"
    ),
    session_name: Optional[str] = typer.Option(
        None,
        help="Name for this session (used in saved session file)"
    )
):
    """Start an interactive chat session with the agent."""
    try:
        # Create progress for agent initialization
        progress = Progress(
            SpinnerColumn(),
            TextColumn("[bold green]{task.description}"),
            BarColumn(bar_width=40),
            TaskProgressColumn(),
            TimeElapsedColumn(),
            console=console
        )
        
        agent_task = None
        
        # Progress callback function
        def progress_callback(message, value):
            nonlocal agent_task
            if agent_task is not None:
                progress.update(agent_task, description=message, completed=int(value * 100))
        
        with progress:
            # Add a task for agent initialization
            agent_task = progress.add_task("[bold green]Initializing agent...", total=100)
            
            # Setup tools
            tool_list = tools.split(",") if tools else []
            tool_directories = tool_dirs.split(",") if tool_dirs else None
            
            # Create the agent with progress reporting
            base_agent = create_agent(
                model_type, model_id, api_key, tool_list, imports, 
                tool_local, tool_hub, tool_space, tool_collection,
                tool_directories, progress_callback=progress_callback
            )
            
            # Create enhanced agent
            agent = EnhancedAgent(base_agent)
            
            # Mark initialization as complete
            progress.update(agent_task, completed=100)
        
        # Load conversation history
        history = [] if no_history else load_conversation_history()
        if history and not no_history:
            console.print(f"[bold green]Loaded conversation history with {len(history)} messages[/bold green]")
        
        # Create a session file if a name is provided
        session_file = create_session_file(session_name) if session_name else None
        
        # Initialize session history
        session_history = []
            
        console.print("\n[bold blue]Interactive Chat Mode[/bold blue]")
        console.print("[green]Type 'exit', 'quit', or use Ctrl+C to end the session[/green]")
        console.print("[green]Type 'history' to view conversation history[/green]")
        console.print("[green]Type 'clear' to clear the conversation history[/green]")
        console.print("[green]Type 'save' to save the current session[/green]\n")
        
        # Main chat loop
        while True:
            try:
                # Get user input
                user_input = typer.prompt("You")
                
                # Check for exit commands
                if user_input.lower() in ["exit", "quit"]:
                    console.print("[bold blue]Exiting chat session[/bold blue]")
                    # Save session on exit if a name was provided
                    if session_name and session_file and session_history:
                        save_session(session_file, session_history, {
                            "model_type": model_type,
                            "model_id": model_id,
                            "output_format": output_format,
                            "timestamp": datetime.now().isoformat()
                        })
                        console.print(f"[green]Session saved to {session_file}[/green]")
                    break
                
                # Check for history command
                if user_input.lower() == "history":
                    if not history:
                        console.print("[yellow]No conversation history yet.[/yellow]")
                    else:
                        for idx, entry in enumerate(history):
                            role = "[bold cyan]You[/bold cyan]" if entry["role"] == "user" else "[bold green]Agent[/bold green]"
                            console.print(f"{idx+1}. {role}: {entry['content'][:100]}{'...' if len(entry['content']) > 100 else ''}")
                    continue
                
                # Check for clear command
                if user_input.lower() == "clear":
                    history = []
                    agent.clear_history()
                    session_history = []
                    console.print("[yellow]Conversation history cleared.[/yellow]")
                    continue
                
                # Check for save command
                if user_input.lower() == "save":
                    if not session_history:
                        console.print("[yellow]No conversation to save yet.[/yellow]")
                        continue
                    
                    save_file = session_file or create_session_file(session_name)
                    save_session(save_file, session_history, {
                        "model_type": model_type,
                        "model_id": model_id,
                        "output_format": output_format,
                        "timestamp": datetime.now().isoformat()
                    })
                    console.print(f"[green]Session saved to {save_file}[/green]")
                    continue
                
                # Process normal input
                history.append({"role": "user", "content": user_input})
                session_history.append({"role": "user", "content": user_input})
                
                # Create a context string from history
                include_history = len(history) > 1
                
                # Run the agent with progress indicator
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[cyan]{task.description}"),
                    TimeElapsedColumn(),
                    console=console
                ) as run_progress:
                    run_task = run_progress.add_task("[cyan]Processing...", total=None)
                    
                    # Define callback for updating progress
                    def run_progress_callback(msg, val):
                        run_progress.update(run_task, description=f"[cyan]{msg}")
                    
                    # Run the agent with context and history
                    response = agent.run(
                        user_input, 
                        include_history=include_history,
                        progress_callback=run_progress_callback
                    )
                    
                    run_progress.update(run_task, completed=True, description="[green]Response ready")
                
                # Display response in the requested format
                print_formatted_response(response, output_format)
                
                # Add to histories
                history.append({"role": "assistant", "content": response})
                session_history.append({"role": "assistant", "content": response})
                
                # Save history if not disabled
                if not no_history:
                    save_conversation_history(history)
                    
            except KeyboardInterrupt:
                console.print("\n[bold blue]Chat session interrupted[/bold blue]")
                break
            except Exception as e:
                console.print(f"[bold red]Error during chat: {str(e)}[/bold red]")
                console.print("[green]You can continue chatting or type 'exit' to quit[/green]")
    
    except AuthenticationError as e:
        print_auth_error(str(e), e.recovery_hint)
        sys.exit(1)
    except ModelNotFoundError as e:
        print_error_panel("Model Not Found", str(e), "Model Error", e.recovery_hint)
        sys.exit(1)
    except Exception as e:
        print_error_panel("Unexpected Error", str(e), "Unhandled Error", 
                         "Please report this issue to the Xerus developers")
        sys.exit(1)

@app.command(name="sessions")
def list_sessions():
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

@app.command(name="load")
def load_session_command(
    session_file: str = typer.Argument(..., help="Name or path of the session file to load"),
    output_format: str = typer.Option(
        "rich", 
        help="Output format (rich, plain, json, markdown)"
    )
):
    """Load and display a saved session."""
    try:
        # Resolve the session file path
        session_dir = get_session_dir()
        session_path = None
        
        # If just a name was provided, find it in the sessions directory
        if not os.path.isfile(session_file):
            # Try exact match
            potential_path = session_dir / session_file
            if potential_path.exists():
                session_path = potential_path
            else:
                # Try adding .json extension
                potential_path = session_dir / f"{session_file}.json"
                if potential_path.exists():
                    session_path = potential_path
                else:
                    # Look for partial matches
                    matches = list(session_dir.glob(f"*{session_file}*.json"))
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
            session_path = Path(session_file)
        
        if not session_path or not session_path.exists():
            console.print(f"[red]Session file '{session_file}' not found.[/red]")
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
                if output_format == "rich":
                    console.print(Markdown(content))
                elif output_format == "plain":
                    console.print(content)
                elif output_format == "json":
                    console.print(json.dumps({"response": content}, indent=2))
                elif output_format == "markdown":
                    console.print(Markdown(content))
    
    except Exception as e:
        console.print(f"[red]Error loading session: {str(e)}[/red]")

def cli():
    """Main entry point for the CLI."""
    app()

if __name__ == "__main__":
    cli() 