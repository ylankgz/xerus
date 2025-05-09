"""
CLI module for Xerus package.
"""
import os
import sys
import typer
from typing import List, Optional
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.progress import Progress
from rich.text import Text
from rich.table import Table

from smolagents import CodeAgent
from smolagents.models import InferenceClientModel, OpenAIServerModel, LiteLLMModel, TransformersModel
from smolagents import WebSearchTool

from . import __version__

app = typer.Typer(add_completion=False)
console = Console()

# ASCII art for Xerus
XERUS_ASCII = """
                    ,;      
                   ;;;      
           .=',    ;:;,     
          /_', "=. ';:;     
          @=:__,  \,;:;     
            _(\.=  ;:;      
           ""_(  _/"        
             '"'''          
"""

def get_model(model_type, model_id, api_key=None):
    """
    Create a model instance based on specified type.
    
    Args:
        model_type: Type of model to use ('inference', 'openai', 'litellm', 'transformers')
        model_id: ID or name of the model
        api_key: API key for the model service
    
    Returns:
        The initialized model instance
    """
    if model_type == "inference":
        return InferenceClientModel(model_id=model_id)
    elif model_type == "openai":
        return OpenAIServerModel(
            model_id=model_id,
            api_key=api_key or os.environ.get("OPENAI_API_KEY")
        )
    elif model_type == "litellm":
        return LiteLLMModel(
            model_id=model_id,
            api_key=api_key or os.environ.get("LITELLM_API_KEY")
        )
    elif model_type == "transformers":
        return TransformersModel(
            model_id=model_id,
            max_new_tokens=4096,
            device_map="auto"
        )
    else:
        raise ValueError(f"Unknown model type: {model_type}")

def create_agent(model_type, model_id, api_key=None, tools=None, imports=None):
    """
    Create a CodeAgent with specified model and tools.
    
    Args:
        model_type: Type of model to use
        model_id: ID or name of the model
        api_key: API key for the model service
        tools: List of tools to enable
        imports: List of Python packages to authorize for import
    
    Returns:
        The initialized CodeAgent
    """
    model = get_model(model_type, model_id, api_key)
    
    available_tools = []
    if tools:
        if "web_search" in tools:
            available_tools.append(WebSearchTool())
    
    additional_imports = []
    if imports:
        additional_imports.extend(imports.split())
    
    return CodeAgent(
        tools=available_tools,
        model=model, 
        additional_authorized_imports=additional_imports
    )

def print_welcome():
    """Print the welcome message with ASCII art"""
    console.print(Panel.fit(
        Text(XERUS_ASCII),
        title="Xerus - CLI Agent, powered by Smolagents",
        border_style="blue"
    ))

def print_project_info():
    """Print information about the Xerus project"""
    # Project description
    description = (
        "Xerus is a command-line interface for running AI agents powered by Huggingface's Smolagents. "
        "It lets you interact with powerful language models through a simple CLI, enabling you to "
        "perform complex tasks, search the web, and execute code."
    )
    
    # Basic usage examples
    examples = [
        ("Basic usage:", "xerus run \"What is the current weather in New York City?\""),
        ("With web search:", "xerus run \"Find the latest news about AI\" --tools web_search"),
        ("With specific imports:", "xerus run \"Create a plot of sin(x)\" --imports numpy,matplotlib"),
        ("Use OpenAI model:", "xerus run \"Explain quantum computing\" --model-type openai --model-id gpt-4"),
    ]
    
    # Create the display panel
    console.print(Panel.fit(
        Text(description),
        title="About Xerus",
        border_style="blue"
    ))
    
    # Display version info
    console.print(f"[bold]Version:[/bold] {__version__}")
    
    # Display examples
    console.print("\n[bold]Examples:[/bold]")
    table = Table(show_header=False, box=None, padding=(0, 2))
    for label, cmd in examples:
        table.add_row(f"[bold]{label}[/bold]", f"[green]{cmd}[/green]")
    console.print(table)
    
    # Commands help
    console.print("\n[bold]Commands:[/bold]")
    console.print("  [green]xerus run[/green]         Run the agent with a prompt")
    console.print("  [green]xerus --help[/green]      Show help message")

@app.callback(invoke_without_command=True)
def callback(ctx: typer.Context):
    """Xerus CLI - An AI agent powered by Smolagents"""
    print_welcome()
    
    # If no subcommand is provided, show project info
    if ctx.invoked_subcommand is None:
        print_project_info()

@app.command(name="run")
def run(
    prompt: str = typer.Argument(..., help="Text instruction for the agent to process"),
    model_type: str = typer.Option(
        "inference", 
        help="Type of model to use (inference, openai, litellm, or transformers)"
    ),
    model_id: str = typer.Option(
        "Qwen/Qwen2.5-Coder-32B-Instruct",
        help="ID or name of the model"
    ),
    api_key: Optional[str] = typer.Option(
        None, 
        help="API key for the model service"
    ),
    tools: Optional[str] = typer.Option(
        None,
        help="Comma-separated list of tools to enable (e.g., web_search)"
    ),
    imports: Optional[str] = typer.Option(
        None,
        help="Space-separated list of Python packages to authorize for import"
    )
):
    """Run the agent with a prompt."""
    try:
        # Add validation for model_type
        valid_model_types = ["inference", "openai", "litellm", "transformers"]
        if model_type not in valid_model_types:
            raise ValueError(f"Invalid model type: {model_type}. Must be one of: {', '.join(valid_model_types)}")
            
        with console.status("[bold green]Initializing agent..."):
            tool_list = tools.split(",") if tools else []
            agent = create_agent(model_type, model_id, api_key, tool_list, imports)
        
        console.print(Panel.fit(
            f"[bold]Prompt:[/bold] {prompt}",
            title="Xerus Agent",
            border_style="blue"
        ))
        
        with Progress() as progress:
            task = progress.add_task("[cyan]Running agent...", total=None)
            
            # Run the agent
            response = agent.run(prompt)
        
        console.print(Panel.fit(
            Markdown(response),
            title="Agent Response",
            border_style="green"
        ))
    
    except Exception as e:
        error_message = str(e)
        if "401 Client Error: Unauthorized" in error_message and "Invalid username or password" in error_message:
            console.print(Panel.fit(
                "[bold red]Authentication Error:[/bold red] Unable to authenticate with Hugging Face.\n\n"
                "To use Hugging Face models, you need to set your HF_TOKEN environment variable:\n"
                "  export HF_TOKEN=your_huggingface_token\n\n"
                "You can get your token from: https://huggingface.co/settings/tokens",
                title="Authentication Error",
                border_style="red"
            ))
        else:
            console.print(Panel.fit(
                f"[bold red]Error:[/bold red] {error_message}",
                title="Error",
                border_style="red"
            ))
        sys.exit(1)

def cli():
    """Main entry point for the CLI."""
    app()

if __name__ == "__main__":
    cli() 