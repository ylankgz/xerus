"""
CLI module for Xerus package.
"""
import os
import sys
import typer
from typing import List, Optional
from rich.console import Console
from rich.progress import Progress

from . import __version__
from .agent import create_agent
from .display import (
    console, print_welcome, print_project_info, print_prompt_panel,
    print_response_panel, print_error_panel, print_auth_error
)
from .models import XerusError, ModelInitializationError, AuthenticationError

app = typer.Typer(add_completion=False)

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
        help="Comma-separated list of tools to enable (currently supported: web_search)"
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
        help="Comma-separated list of tools to enable (currently supported: web_search)"
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
        help="Hugging Face Space ID to import as a tool"
    ),
    tool_collection: Optional[str] = typer.Option(
        None,
        help="Hugging Face Hub repo ID for a collection of tools"
    )
):
    """Run the agent with a prompt."""
    try:
        with console.status("[bold green]Initializing agent..."):
            tool_list = tools.split(",") if tools else []
            agent = create_agent(model_type, model_id, api_key, tool_list, imports, 
                               tool_local, tool_hub, tool_space, tool_collection)
        
        print_prompt_panel(prompt)
        
        with Progress() as progress:
            task = progress.add_task("[cyan]Running agent...", total=None)
            
            # Run the agent
            response = agent.run(prompt)
        
        print_response_panel(response)
    
    except AuthenticationError as e:
        print_auth_error(str(e))
        sys.exit(1)
    except ModelInitializationError as e:
        print_error_panel("Model Error", str(e), "Model Initialization Failed")
        sys.exit(1)
    except XerusError as e:
        print_error_panel("Xerus Error", str(e))
        sys.exit(1)
    except Exception as e:
        print_error_panel("Unexpected Error", str(e))
        sys.exit(1)

def cli():
    """Main entry point for the CLI."""
    app()

if __name__ == "__main__":
    cli() 