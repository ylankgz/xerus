"""
Display module for Xerus package.
"""
import json
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
        ("Use OpenAI model:", "xerus run \"Explain quantum computing\" --model-type openai --model-id gpt-4 --api-key YOUR_API_KEY"),
        ("Use Mixtral model:", "xerus run \"Write a Python script\" --model-type inference --model-id mistralai/Mixtral-8x7B-Instruct-v0.1"),
        ("Use local MLX model:", "xerus run \"Summarize text\" --model-type mlx-lm --model-id mlx-community/Mistral-7B-Instruct-v0.1-mlx"),
        ("With local tool:", "xerus run \"Generate image\" --tool-local ./my_tools.py"),
        ("With Hub tool:", "xerus run \"Analyze sentiment\" --tool-hub username/sentiment-tool"),
        ("With Space tool:", "xerus run \"Generate an image\" --tool-space stabilityai/stable-diffusion:image_generator:Generates images from text prompts"),
        ("With tool collection:", "xerus run \"Analyze data\" --tool-collection huggingface-tools/data-analysis"),
        ("Interactive mode:", "xerus chat --tools web_search"),
        ("Change output format:", "xerus run \"Tell me a joke\" --output-format json"),
        ("Save session:", "xerus run \"Explain relativity\" --save-session"),
        ("Named session:", "xerus chat --session-name physics"),
        ("Custom API endpoint:", "xerus run \"Explain RLHF\" --model-type openai --api-base https://your-api-endpoint.com/v1"),
        ("List sessions:", "xerus sessions"),
        ("Load session:", "xerus load physics_20230615_123045")
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
        "--api-key", 
        "API key for model service (alternatively use environment variables)"
    )
    options_table.add_row(
        "--api-base", 
        "Base URL for API (for OpenAI and similar APIs)"
    )
    options_table.add_row(
        "--organization", 
        "Organization ID (for OpenAI)"
    )
    options_table.add_row(
        "--project", 
        "Project ID (for some API providers)"
    )
    options_table.add_row(
        "--client-kwargs", 
        "JSON string of additional client arguments (for API clients)"
    )
    options_table.add_row(
        "--custom-role-conversions", 
        "JSON string of role conversion mappings (for OpenAI)"
    )
    options_table.add_row(
        "--flatten-messages-as-text", 
        "Whether to flatten messages as text (for OpenAI)"
    )
    options_table.add_row(
        "--tool-name-key", 
        "The key for retrieving a tool name (for transformers/MLX models)"
    )
    options_table.add_row(
        "--tool-arguments-key", 
        "The key for retrieving tool arguments (for transformers/MLX models)"
    )
    options_table.add_row(
        "--trust-remote-code", 
        "Whether to trust remote code for models (for transformers/MLX models)"
    )
    options_table.add_row(
        "--tools", 
        "Comma-separated tools list (currently supported: web_search, python_interpreter, final_answer, user_input, duckduckgo_search, google_search, visit_webpage)"
    )
    options_table.add_row(
        "--imports", 
        "Space-separated Python packages the agent can import (e.g., \"numpy matplotlib pandas\")"
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
    options_table.add_row(
        "--output-format", 
        "Output format (rich, plain, json, markdown)"
    )
    options_table.add_row(
        "--session-name", 
        "Name for the current session (used in saved session files)"
    )
    options_table.add_row(
        "--save-session", 
        "Save the current session to a file for later reference"
    )
    options_table.add_row(
        "--no-history", 
        "Don't load or save conversation history in chat mode"
    )
    console.print(options_table)
    
    # Commands help
    console.print("\n[bold]Commands:[/bold]")
    console.print("  [green]xerus run[/green]         Run the agent with a prompt")
    console.print("  [green]xerus chat[/green]        Start an interactive chat session")
    console.print("  [green]xerus sessions[/green]    List all saved sessions")
    console.print("  [green]xerus load[/green]        Load and display a saved session")
    console.print("  [green]xerus --help[/green]      Show help message")

def print_response_panel(response):
    """Print the agent response panel"""
    console.print(Panel(
        Markdown(response),
        title="Agent Response",
        border_style="green"
    ))

def print_formatted_response(response, format_type="rich"):
    """
    Print the agent response in the specified format
    
    Args:
        response: The response text from the agent
        format_type: Format type (rich, plain, json, markdown)
    """
    format_type = format_type.lower()
    
    if format_type == "rich":
        print_response_panel(response)
    elif format_type == "plain":
        console.print("\n--- Agent Response ---")
        console.print(response)
        console.print("---------------------\n")
    elif format_type == "json":
        # Format as JSON with the response as a string
        json_response = {
            "response": response
        }
        console.print(json.dumps(json_response, indent=2))
    elif format_type == "markdown":
        console.print(Markdown(response))
    else:
        # Default to rich format if unknown format specified
        console.print("[yellow]Unknown format type. Using rich format.[/yellow]")
        print_response_panel(response)

def print_error_panel(error_type, error_message, title="Error", recovery_hint=None):
    """
    Print an error panel with optional recovery hint
    
    Args:
        error_type: Type of error
        error_message: The error message
        title: Panel title
        recovery_hint: Optional recovery hint to help the user resolve the issue
    """
    content = f"[bold red]{error_type}:[/bold red] {error_message}"
    
    if recovery_hint:
        content += f"\n\n[bold yellow]Recovery Hint:[/bold yellow] {recovery_hint}"
    
    console.print(Panel.fit(
        content,
        title=title,
        border_style="red"
    ))

def print_auth_error(error_message, recovery_hint=None):
    """
    Print authentication error panel with help text
    
    Args:
        error_message: The error message
        recovery_hint: Optional recovery hint
    """
    hint = recovery_hint or (
        "To use Hugging Face models, you need to set your HF_TOKEN environment variable:\n"
        "  export HF_TOKEN=your_huggingface_token\n\n"
        "To use OpenAI models, set your OPENAI_API_KEY environment variable:\n"
        "  export OPENAI_API_KEY=your_openai_api_key\n\n"
        "You can also provide these directly with the --api-key argument."
    )
    
    console.print(Panel.fit(
        f"[bold red]Authentication Error:[/bold red] {error_message}\n\n"
        f"[bold yellow]Recovery Hint:[/bold yellow] {hint}",
        title="Authentication Error",
        border_style="red"
    )) 