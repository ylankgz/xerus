"""
Main CLI application for Xerus.
"""
import sys
import warnings
import typer
from typing import Optional

# Try to load environment variables from .env file if python-dotenv is installed
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # Not raising an error since dotenv is optional
    warnings.warn(
        "python-dotenv package not installed. Environment variables from .env files will not be loaded. "
        "Install with: pip install python-dotenv"
    )

from .. import __version__
from ..display import print_welcome, print_project_info
from .commands import (
    run_command, chat_command, list_sessions_command, load_session_command
)

def _parse_param_value(value):
    """
    Parse string parameter values into appropriate Python types.
    
    Args:
        value: The string value to parse
        
    Returns:
        The parsed value as the appropriate type (str, int, float, bool)
    """
    # Check if value is a boolean
    if value.lower() in ('true', 'yes', 'y'):
        return True
    if value.lower() in ('false', 'no', 'n'):
        return False
    
    # Check if value is a number
    try:
        # Try converting to int first
        return int(value)
    except ValueError:
        try:
            # Then try float
            return float(value)
        except ValueError:
            # Otherwise, return as string
            return value

app = typer.Typer(add_completion=False)

# Export the run function for backward compatibility
run = run_command

@app.callback(invoke_without_command=True)
def callback(
    ctx: typer.Context,
    model_id: Optional[str] = typer.Option(
        None,
        help="Model identifier (e.g., 'Qwen/Qwen2.5-Coder-32B-Instruct', 'gpt-4', 'mistralai/Mistral-7B-Instruct-v0.1')"
    ),
    api_key: Optional[str] = typer.Option(
        None, 
        help="API key for the model service (can also use environment variables like OPENAI_API_KEY)"
    ),
    api_base: Optional[str] = typer.Option(
        None,
        help="Base URL for API (for OpenAI and similar APIs)"
    ),
    tool_name_key: Optional[str] = typer.Option(
        None,
        help="The key for retrieving a tool name (for transformers/MLX models)"
    ),
    tool_arguments_key: Optional[str] = typer.Option(
        None,
        help="The key for retrieving tool arguments (for transformers/MLX models)"
    ),
    extra_params: Optional[list[str]] = typer.Option(
        None,
        help="Extra parameters in key=value format (can be specified multiple times). Example: --extra-params=\"temperature=0.7\" --extra-params=\"top_p=0.9\"",
        callback=lambda x: {k.split('=')[0]: _parse_param_value(k.split('=')[1]) for k in x} if x else {}
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
   
    
    # If no subcommand is provided, show project info
    if ctx.invoked_subcommand is None:
        """Xerus CLI - An AI agent powered by Huggingface Smolagents"""
        print_welcome()
        print_project_info()

@app.command(name="run")
def run(
    prompt: Optional[str] = typer.Option(None, "--prompt", "-p", help="Text instruction for the agent to process"),
    model_id: Optional[str] = typer.Option(
        None,
        help="Model identifier (e.g., 'Qwen/Qwen2.5-Coder-32B-Instruct', 'gpt-4', 'mistralai/Mistral-7B-Instruct-v0.1')"
    ),
    api_key: Optional[str] = typer.Option(
        None,
        help="API key for the model service (can also use environment variables like OPENAI_API_KEY)"
    ),
    api_base: Optional[str] = typer.Option(
        None,
        help="Base URL for API (for OpenAI and similar APIs)"
    ),
    custom_role_conversions: Optional[str] = typer.Option(
        None,
        help="JSON string of role conversion mappings (for OpenAI)"
    ),
    flatten_messages_as_text: Optional[bool] = typer.Option(
        False,
        help="Whether to flatten messages as text (for OpenAI)"
    ),
    tool_name_key: Optional[str] = typer.Option(
        None,
        help="The key for retrieving a tool name (for transformers/MLX models)"
    ),
    tool_arguments_key: Optional[str] = typer.Option(
        None,
        help="The key for retrieving tool arguments (for transformers/MLX models)"
    ),
    extra_params: Optional[list[str]] = typer.Option(
        None,
        help="Extra parameters in key=value format (can be specified multiple times). Example: --extra-params=\"temperature=0.7\" --extra-params=\"top_p=0.9\"",
        callback=lambda x: {k.split('=')[0]: _parse_param_value(k.split('=')[1]) for k in x} if x else {}
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
    run_command(
        prompt=prompt, 
        model_id=model_id, 
        api_key=api_key,
        api_base=api_base,
        custom_role_conversions=custom_role_conversions,
        flatten_messages_as_text=flatten_messages_as_text,
        tool_name_key=tool_name_key,
        tool_arguments_key=tool_arguments_key,
        extra_params=extra_params,
        tools=tools,
        imports=imports,
        tool_local=tool_local,
        tool_hub=tool_hub,
        tool_space=tool_space,
        tool_collection=tool_collection,
        tool_dirs=tool_dirs,
        output_format=output_format,
        save_session=save_session
    )

@app.command(name="chat")
def chat(
    model_id: Optional[str] = typer.Option(
        None,
        help="Model identifier (e.g., 'Qwen/Qwen2.5-Coder-32B-Instruct', 'gpt-4', 'mistralai/Mistral-7B-Instruct-v0.1')"
    ),
    api_key: Optional[str] = typer.Option(
        None,
        help="API key for the model service (can also use environment variables like OPENAI_API_KEY)"
    ),
    api_base: Optional[str] = typer.Option(
        None,
        help="Base URL for API (for OpenAI and similar APIs)"
    ),
    custom_role_conversions: Optional[str] = typer.Option(
        None,
        help="JSON string of role conversion mappings (for OpenAI)"
    ),
    flatten_messages_as_text: bool = typer.Option(
        False,
        help="Whether to flatten messages as text (for OpenAI)"
    ),
    tool_name_key: Optional[str] = typer.Option(
        None,
        help="The key for retrieving a tool name (for transformers/MLX models)"
    ),
    tool_arguments_key: Optional[str] = typer.Option(
        None,
        help="The key for retrieving tool arguments (for transformers/MLX models)"
    ),
    extra_params: Optional[list[str]] = typer.Option(
        None,
        help="Extra parameters in key=value format (can be specified multiple times). Example: --extra-params=\"temperature=0.7\" --extra-params=\"top_p=0.9\"",
        callback=lambda x: {k.split('=')[0]: _parse_param_value(k.split('=')[1]) for k in x} if x else {}
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
        help="Name for this session (used in saved session file)"
    )
):
    """Start an interactive chat session with the agent."""
    chat_command(
        model_id=model_id,
        api_key=api_key,
        api_base=api_base,
        custom_role_conversions=custom_role_conversions,
        flatten_messages_as_text=flatten_messages_as_text,
        tool_name_key=tool_name_key,
        tool_arguments_key=tool_arguments_key,
        extra_params=extra_params,
        tools=tools,
        imports=imports,
        tool_local=tool_local,
        tool_hub=tool_hub,
        tool_space=tool_space,
        tool_collection=tool_collection,
        tool_dirs=tool_dirs,
        output_format=output_format,
        no_history=no_history,
        session_name=session_name
    )

@app.command(name="sessions")
def sessions():
    """List all saved sessions."""
    list_sessions_command()

@app.command(name="load")
def load(
    session_file: Optional[str] = typer.Option(None, "--session", "-s", help="Name or path of the session file to load"),
    output_format: str = typer.Option(
        "rich", 
        help="Output format (rich, plain, json, markdown)"
    )
):
    """Load and display a saved session."""
    load_session_command(session_file, output_format)

def cli():
    """Main entry point for the CLI."""
    app() 