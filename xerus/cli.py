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
import importlib

from smolagents import CodeAgent
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
    # Map model_type to the corresponding class name
    model_class_map = {
        "inference": "InferenceClientModel",
        "openai": "OpenAIServerModel",
        "azure-openai": "AzureOpenAIServerModel",
        "amazon-bedrock": "AmazonBedrockServerModel",
        "mlx-lm": "MLXModel",
        "litellm": "LiteLLMModel",
        "transformers": "TransformersModel"
    }
    
    if model_type not in model_class_map:
        raise ValueError(f"Unknown model type: {model_type}")
    
    # Dynamically import the appropriate model class
    model_class_name = model_class_map[model_type]
    ModelClass = getattr(importlib.import_module("smolagents.models"), model_class_name)
    
    # Initialize and return the model based on its type
    if model_type == "inference":
        return ModelClass(model_id=model_id)
    elif model_type in ["openai", "azure-openai"]:
        return ModelClass(
            model_id=model_id,
            api_key=api_key or os.environ.get("OPENAI_API_KEY")
        )
    elif model_type == "amazon-bedrock":
        return ModelClass(
            model_id=model_id,
            aws_access_key=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
            aws_region=os.environ.get("AWS_REGION", "us-east-1")
        )
    elif model_type == "litellm":
        return ModelClass(
            model_id=model_id,
            api_key=api_key or os.environ.get("LITELLM_API_KEY")
        )
    elif model_type == "transformers":
        return ModelClass(
            model_id=model_id,
            max_new_tokens=4096,
            device_map="auto"
        )
    elif model_type == "mlx-lm":
        return ModelClass(
            model_id=model_id,
            max_tokens=4096
        )

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
        help="Type of model to use (inference, openai, azure-openai, amazon-bedrock, litellm, transformers, mlx-lm)"
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
        # Get the list of valid model types from the model_class_map
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
        if "401 Client Error: Unauthorized" in error_message:
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