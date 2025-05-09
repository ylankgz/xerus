"""
Display module for Xerus package.
"""
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.text import Text
from rich.table import Table

from . import __version__

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

def print_prompt_panel(prompt):
    """Print the prompt panel"""
    console.print(Panel.fit(
        f"[bold]Prompt:[/bold] {prompt}",
        title="Xerus Agent",
        border_style="blue"
    ))

def print_response_panel(response):
    """Print the agent response panel"""
    console.print(Panel.fit(
        Markdown(response),
        title="Agent Response",
        border_style="green"
    ))

def print_error_panel(error_type, error_message, title="Error"):
    """Print an error panel"""
    console.print(Panel.fit(
        f"[bold red]{error_type}:[/bold red] {error_message}",
        title=title,
        border_style="red"
    ))

def print_auth_error(error_message):
    """Print authentication error panel with help text"""
    console.print(Panel.fit(
        f"[bold red]Authentication Error:[/bold red] {error_message}\n\n"
        "To use Hugging Face models, you need to set your HF_TOKEN environment variable:\n"
        "  export HF_TOKEN=your_huggingface_token\n\n"
        "You can get your token from: https://huggingface.co/settings/tokens",
        title="Authentication Error",
        border_style="red"
    )) 