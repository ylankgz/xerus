import os
import json
from typing import Optional
import rich_click as click

from ..agent import EnhancedAgent
from ..error_handler import handle_command_errors
from ..model import ModelFactory
from ..sessions import (
    create_session_file,
    save_session
)
from ..tools import setup_built_in_tools
from ..ui.display import console
from ..ui.progress import create_initialization_progress
from ..utils import parse_kwargs
from smolagents import CodeAgent, LogLevel

@click.command()
@click.option("--model-id", help="[bold]Model identifier[/bold] (e.g. gpt-4, claude-2)")
@click.option("--api-key", help="[bold]API key[/bold] for the service")
@click.option("--api-base", help="[italic]Custom[/italic] API base URL")
@click.option("--session-name", help="Name for this session (used in saved session file)")
@click.argument("kwargs", nargs=-1, type=click.UNPROCESSED)
@handle_command_errors
def chat(
    model_id,
    api_key,
    api_base,
    session_name: Optional[str],
    kwargs,
):
    """[bold]Interactive chat with AI model[/bold] with given parameters.

    Examples:\n
    [green]xerus chat --model-id gpt-4 --api-key sk-123[/green]\n
    [green]xerus chat --session-name "My session" --help[/green] to see all available options \n
    """
    # Create a progress instance for initialization
    progress = create_initialization_progress()
    
    agent_task = None

    with progress:
        # Add a task for agent initialization
        agent_task = progress.add_task("[bold green]Initializing agent...", total=100)

        # Setup built-in tools
        built_in_tools_agents_list = setup_built_in_tools()

        client = ModelFactory.create_client(
            model_id=model_id or "openai/deepseek-ai/DeepSeek-R1-0528",
            api_key=api_key or os.environ.get("GMI_CLOUD_API_KEY"),
            api_base=api_base or "https://api.gmi-serving.com/v1",
            **parse_kwargs(kwargs)
        )

        # Create manager agent
        manager_agent = CodeAgent(
            tools=[],
            model=client,
            managed_agents=[
                *built_in_tools_agents_list,
            ],
            # additional_authorized_imports=["*"],
            max_steps=10,
            verbosity_level=2,
            name="xerus_manager_agent",
            description="Analyzes, trains, fine-tunes and runs ML models"
        )

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
                    save_session(session_file, session_history, {
                        "model_id": model_id,
                    })
                    console.print(f"[green]Session saved to {session_file}[/green]")
                break
            
            # Check for save command
            if user_input.lower() == "save":
                if not session_history:
                    console.print("[yellow]No conversation to save yet.[/yellow]")
                    continue
                
                save_file = session_file or create_session_file(session_name)
                save_session(save_file, session_history, {
                    "model_id": model_id,
                })
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