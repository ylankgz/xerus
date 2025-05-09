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
import importlib.util

from smolagents import CodeAgent
from smolagents import WebSearchTool
from smolagents import Tool, load_tool, ToolCollection

from . import __version__
from .models import get_model, XerusError, ModelInitializationError, AuthenticationError

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

def create_agent(model_type, model_id, api_key=None, tools=None, imports=None, 
               tool_local=None, tool_hub=None, tool_space=None, tool_collection=None):
    """
    Create a CodeAgent with specified model and tools.
    
    Args:
        model_type: Type of model to use
        model_id: ID or name of the model
        api_key: API key for the model service
        tools: List of tools to enable
        imports: List of Python packages to authorize for import
        tool_local: Path to a local tool file
        tool_hub: Hugging Face Hub repo ID for a tool
        tool_space: Hugging Face Space ID to import as a tool
        tool_collection: Hugging Face Hub repo ID for a collection of tools
    
    Returns:
        The initialized CodeAgent
    """
    model = get_model(model_type, model_id, api_key)
    
    available_tools = []
    if tools:
        if "web_search" in tools:
            available_tools.append(WebSearchTool())
    
    # Add tool from local file if specified
    if tool_local:
        try:
            console.print(f"[bold blue]Loading tool from local file: {tool_local}[/bold blue]")
            # Import the module dynamically
            spec = importlib.util.spec_from_file_location("local_tool", tool_local)
            local_tool_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(local_tool_module)
            
            # Find Tool instances in the module
            for name in dir(local_tool_module):
                obj = getattr(local_tool_module, name)
                if isinstance(obj, Tool):
                    available_tools.append(obj)
                    console.print(f"[green]Successfully loaded tool: {obj.name}[/green]")
        except Exception as e:
            console.print(f"[red]Error loading tool from local file: {str(e)}[/red]")
    
    # Add tool from Hugging Face Hub if specified
    if tool_hub:
        try:
            console.print(f"[bold blue]Loading tool from Hugging Face Hub: {tool_hub}[/bold blue]")
            hub_tool = load_tool(tool_hub, trust_remote_code=True)
            available_tools.append(hub_tool)
            console.print(f"[green]Successfully loaded tool from Hub: {hub_tool.name}[/green]")
        except Exception as e:
            console.print(f"[red]Error loading tool from Hub: {str(e)}[/red]")
    
    # Add tool from Hugging Face Space if specified
    if tool_space:
        try:
            # Extract name and description if provided in format "space_id:name:description"
            parts = tool_space.split(":", 2)
            space_id = parts[0]
            name = parts[1] if len(parts) > 1 else "space_tool"
            description = parts[2] if len(parts) > 2 else f"Tool from Space {space_id}"
            
            console.print(f"[bold blue]Loading tool from Hugging Face Space: {space_id}[/bold blue]")
            space_tool = Tool.from_space(space_id, name=name, description=description)
            available_tools.append(space_tool)
            console.print(f"[green]Successfully loaded tool from Space: {name}[/green]")
        except Exception as e:
            console.print(f"[red]Error loading tool from Space: {str(e)}[/red]")
    
    # Add tools from collection if specified
    if tool_collection:
        try:
            console.print(f"[bold blue]Loading tool collection from Hub: {tool_collection}[/bold blue]")
            collection = ToolCollection.from_hub(collection_slug=tool_collection, trust_remote_code=True)
            # Add all tools from the collection
            available_tools.extend(collection.tools)
            console.print(f"[green]Successfully loaded tool collection with {len(collection.tools)} tools[/green]")
        except Exception as e:
            console.print(f"[red]Error loading tool collection: {str(e)}[/red]")
    
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
        title="Xerus - CLI Agent, powered by Huggingface Smolagents",
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
        ("With specific imports:", "xerus run \"Create a plot of sin(x)\" --imports \"numpy matplotlib\""),
        ("Use OpenAI model:", "xerus run \"Explain quantum computing\" --model-type openai --model-id gpt-4"),
        ("Use Mixtral model:", "xerus run \"Write a Python script\" --model-type inference --model-id mistralai/Mixtral-8x7B-Instruct-v0.1"),
        ("With local tool:", "xerus run \"Generate image\" --tool-local ./my_tools.py"),
        ("With Hub tool:", "xerus run \"Analyze sentiment\" --tool-hub username/sentiment-tool"),
        ("With Space tool:", "xerus run \"Generate an image\" --tool-space stabilityai/stable-diffusion:image_generator:Generates images from text prompts"),
        ("With tool collection:", "xerus run \"Analyze data\" --tool-collection huggingface-tools/data-analysis"),
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
    
    # Options help
    console.print("\n[bold]Key Options:[/bold]")
    options_table = Table(show_header=True, box=None, padding=(0, 2))
    options_table.add_column("Option", style="bold green")
    options_table.add_column("Description")
    options_table.add_row(
        "--model-type", 
        "Model provider: inference (HF), openai, azure-openai, amazon-bedrock, litellm, transformers, mlx-lm"
    )
    options_table.add_row(
        "--model-id", 
        "Model identifier (e.g., Qwen/Qwen2.5-Coder-32B-Instruct, gpt-4, mistralai/Mistral-7B-Instruct-v0.1)"
    )
    options_table.add_row(
        "--tools", 
        "Comma-separated tools list (currently supported: web_search)"
    )
    options_table.add_row(
        "--imports", 
        "Space-separated Python packages the agent can import (e.g., \"numpy matplotlib pandas\")"
    )
    options_table.add_row(
        "--api-key", 
        "API key for model service (alternatively use environment variables)"
    )
    options_table.add_row(
        "--tool-local", 
        "Path to a local Python file containing tool definitions"
    )
    options_table.add_row(
        "--tool-hub", 
        "Hugging Face Hub repo ID for a tool (e.g., username/tool-name)"
    )
    options_table.add_row(
        "--tool-space", 
        "Hugging Face Space ID to import as a tool (format: space_id:name:description)"
    )
    options_table.add_row(
        "--tool-collection", 
        "Hugging Face Hub repo ID for a collection of tools"
    )
    console.print(options_table)
    
    # Commands help
    console.print("\n[bold]Commands:[/bold]")
    console.print("  [green]xerus run[/green]         Run the agent with a prompt")
    console.print("  [green]xerus --help[/green]      Show help message")

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
            agent = create_agent(model_type, model_id, api_key, tool_list, imports, tool_local, tool_hub, tool_space, tool_collection)
        
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
    
    except AuthenticationError as e:
        console.print(Panel.fit(
            f"[bold red]Authentication Error:[/bold red] {str(e)}\n\n"
            "To use Hugging Face models, you need to set your HF_TOKEN environment variable:\n"
            "  export HF_TOKEN=your_huggingface_token\n\n"
            "You can get your token from: https://huggingface.co/settings/tokens",
            title="Authentication Error",
            border_style="red"
        ))
        sys.exit(1)
    except ModelInitializationError as e:
        console.print(Panel.fit(
            f"[bold red]Model Error:[/bold red] {str(e)}",
            title="Model Initialization Failed",
            border_style="red"
        ))
        sys.exit(1)
    except XerusError as e:
        console.print(Panel.fit(
            f"[bold red]Xerus Error:[/bold red] {str(e)}",
            title="Error",
            border_style="red"
        ))
        sys.exit(1)
    except Exception as e:
        console.print(Panel.fit(
            f"[bold red]Unexpected Error:[/bold red] {str(e)}",
            title="Error",
            border_style="red"
        ))
        sys.exit(1)

def cli():
    """Main entry point for the CLI."""
    app()

if __name__ == "__main__":
    cli() 