import os
import json
from typing import Optional
import rich_click as click

from ..agent import EnhancedAgent
from ..error_handler import handle_command_errors
from ..errors import InputError
from ..model import ModelFactory
from ..sessions import create_session_file, save_session
from ..tools import setup_built_in_tools, setup_local_tools, setup_huggingface_tools
from ..ui.display import console
from ..ui.progress import create_initialization_progress
from ..utils import parse_kwargs
from smolagents import CodeAgent

@click.command()
@click.option("--prompt", required=True, help="[bold]Input prompt[/bold] for the AI model")
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
@click.option("--save-session", is_flag=True, default=True, help="Save the session to a file")
@click.argument("kwargs", nargs=-1, type=click.UNPROCESSED)
@handle_command_errors
def run(
    prompt, 
    model_id, 
    api_key, 
    api_base, 
    custom_role_conversions, 
    flatten_messages_as_text, 
    kwargs,
    built_in_tools: bool,
    local_tools: Optional[str],
    hub_tools: Optional[str],
    space_tools: Optional[str],
    collection_tools: Optional[str],
    save_session: bool
):
    """[bold]Run AI model[/bold] with given parameters.

    Examples:\n
    [green]xerus run --prompt "Hello" --model-id gpt-4 --api-key sk-123[/green]\n
    [green]xerus run --help[/green] to see all available options \n
    """
    if prompt is None:
        raise InputError("No prompt provided. Please provide a text instruction for the agent to process.")
        
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
        enhanced_agent = EnhancedAgent(manager_agent)

        # Mark initialization as complete
        progress.update(agent_task, completed=100)

        response = enhanced_agent.run(prompt)

        # Save session if requested
        if save_session:
            try:
                session_file = create_session_file()
                save_session(session_file, [
                    {"role": "user", "content": prompt},
                    {"role": "assistant", "content": response}
                ], {
                    "model_id": model_id,
                })
                console.print(f"[green]Session saved to {session_file}[/green]")
            except Exception as e:
                console.print(f"[yellow]Warning: Could not save session: {str(e)}[/yellow]") 