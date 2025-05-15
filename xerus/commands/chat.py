import os
import json
from typing import Optional
import rich_click as click

from ..agent import EnhancedAgent
from ..error_handler import handle_command_errors
from ..model import ModelFactory
from ..sessions import (
    load_conversation_history,
    save_conversation_history,
    create_session_file,
    save_session
)
from ..tools import setup_local_tools, setup_huggingface_tools, setup_built_in_tools
from ..ui.display import console
from ..ui.progress import create_initialization_progress
from ..utils import parse_kwargs
from smolagents import CodeAgent

@click.command()
@click.option("--model-id", help="[bold]Model identifier[/bold] (e.g. gpt-4, claude-2)")
@click.option("--api-key", help="[bold]API key[/bold] for the service")
@click.option("--api-base", help="[italic]Custom[/italic] API base URL")
@click.option("--custom-role-conversions", type=click.Path(exists=True), help="Path to [underline]JSON file[/underline] with role conversions")
@click.option("--flatten-messages-as-text", is_flag=True, help="Flatten messages to [bold]plain text[/bold]")
@click.option("--built-in-tools", is_flag=True, help="Use built-in tools (web_search, python_interpreter, final_answer, user_input, duckduckgo_search, visit_webpage)")
@click.option("--local-tools", help="Path to [underline]local tool file[/underline]")
@click.option("--hub-tools", help="List of HuggingFace Hub repos")
@click.option("--space-tools", help="List of HuggingFace Spaces (format: space_id:name:description)")
@click.option("--collection-tools", help="HuggingFace Hub repo ID for a collection of tools")
@click.option("--no-history", is_flag=True, default=False, help="Do not load conversation history")
@click.option("--session-name", help="Name for this session (used in saved session file)")
@click.argument("kwargs", nargs=-1, type=click.UNPROCESSED)
@handle_command_errors
def chat(
    model_id,
    api_key,
    api_base,
    custom_role_conversions,
    flatten_messages_as_text,
    built_in_tools: bool,
    local_tools: Optional[str],
    hub_tools: Optional[str],
    space_tools: Optional[str],
    collection_tools: Optional[str],
    no_history: bool,
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
        built_in_tools_agents_list = setup_built_in_tools(model_id, api_key, api_base) if built_in_tools else []


        # Setup local tools
        local_tools_agents_list = setup_local_tools(local_tools, model_id, api_key, api_base)
        
        # Setup Hugging Face tools
        space_tools_agents_list, collection_tools_agents_list, hub_tools_agents_list = setup_huggingface_tools(
            model_id, api_key, api_base, hub_tools, space_tools, collection_tools
        )

        # Parse JSON strings for client_kwargs and custom_role_conversions if provided
        role_conversions_dict = json.loads(custom_role_conversions) if custom_role_conversions else None
    
        client = ModelFactory.create_client(
            model_id=model_id or "openai/o4-mini",
            api_key=api_key or os.environ.get("LITELLM_API_KEY"),
            api_base=api_base,
            custom_role_conversions=role_conversions_dict,
            flatten_messages_as_text=flatten_messages_as_text,
            **parse_kwargs(kwargs)
        )

        # Create manager agent
        manager_agent = CodeAgent(
            tools=[],
            model=client,
            managed_agents=[
                *built_in_tools_agents_list,
                *local_tools_agents_list,
                *space_tools_agents_list,
                *collection_tools_agents_list,
                *hub_tools_agents_list
            ],
            name="xerus_manager_agent",
            description="Analyzes, trains, fine-tunes and runs ML models"
        )

        # Create the enhanced agent
        agent = EnhancedAgent(manager_agent)

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
                    "model_id": model_id,
                })
                console.print(f"[green]Session saved to {save_file}[/green]")
                continue
            
            # Process normal input
            history.append({"role": "user", "content": user_input})
            session_history.append({"role": "user", "content": user_input})
            
            # Create a context string from history
            include_history = len(history) > 1
            
            # Run the agent with context and history
            response = agent.run(
                user_input, 
                include_history=include_history,
            )
            
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