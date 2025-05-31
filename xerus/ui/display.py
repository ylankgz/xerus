"""
Display module for Xerus package.
"""
import json
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.text import Text
from rich.table import Table

from .. import __version__

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
        border_style="blue"
    ))

def print_project_info():
    """Print information about the Xerus project"""
    # Project description
    description = (
        "Xerus is a command-line interface for running AI agents powered by Huggingface's Smolagents. "
        "It lets you interact with powerful language models through a simple CLI, enabling you to "
        "perform complex tasks on your data, train and fine-tune ML models and build complex pipelines."
    )
    
    # Basic usage examples
    examples = [
        ("Fine-tune a model:", "xerus run \"Fine-tune BERT on my text classification dataset\""),
        ("Train with GPU:", "xerus run \"Train a CNN with GPU acceleration\" "),
        ("Hyperparameter tuning:", "xerus run \"Optimize hyperparameters for my XGBoost model\""),
        ("Custom model evaluation:", "xerus run \"Evaluate my NLP model on test dataset\""),
        ("Build data pipeline:", "xerus run \"Create a data preprocessing pipeline for my images\""),
        ("ONNX conversion:", "xerus run \"Convert my PyTorch model to ONNX format\""),
        ("Dataset exploration:", "xerus run \"Analyze my tabular dataset\""),
        ("Multi-agent ML chat:", "xerus chat --session-name ml_experiment"),
        ("Interactive debugging:", "xerus chat"),
        ("Save experiment:", "xerus chat --session-name training_run_1"),
        ("Resume training:", "xerus chat --session-name continue_training"),
        ("Deploy trained model:", "xerus run \"Package and deploy my trained model to production\""),
        ("Load experiment:", "xerus load ml_experiment_20230615_123045"),
        ("List all sessions:", "xerus sessions")
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
        "--session-name", 
        "Name for the current session (used in saved session files)"
    )
    options_table.add_row(
        "--prompt", 
        "Input prompt for the AI model (required for run command)"
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