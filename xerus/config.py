import os
import json
import re
from pathlib import Path
from typing import Dict, Any

try:
    from dotenv import load_dotenv
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False

from .ui.display import console


def ensure_config_exists():
    """Ensure ~/.xerus directory and config.json exist, create from template if needed."""
    xerus_dir = os.path.expanduser("~/.xerus")
    config_path = os.path.join(xerus_dir, "config.json")
    
    # Create ~/.xerus directory if it doesn't exist
    if not os.path.exists(xerus_dir):
        os.makedirs(xerus_dir, exist_ok=True)
        console.print(f"[green]Created Xerus config directory: {xerus_dir}[/green]")
    
    # Copy template config if config.json doesn't exist
    if not os.path.exists(config_path):
        try:
            # Get the template from the package directory
            template_path = Path(__file__).parent / 'config_template.json'
            if template_path.exists():
                with open(template_path, 'r') as f:
                    template_content = f.read()
                with open(config_path, 'w') as f:
                    f.write(template_content)
                console.print(f"[green]Created default config file: {config_path}[/green]")
                console.print("[yellow]You can customize tool settings by editing this file[/yellow]")
            else:
                console.print(f"[red]Template config file not found at: {template_path}[/red]")
                console.print("[yellow]Continuing with default hardcoded settings[/yellow]")
        except Exception as e:
            console.print(f"[red]Error creating config file: {e}[/red]")
            console.print("[yellow]Continuing with default hardcoded settings[/yellow]")


def substitute_env_vars(value: Any) -> Any:
    """
    Recursively substitute environment variables in configuration values.
    Supports ${VAR_NAME} syntax.
    """
    if isinstance(value, str):
        # Pattern to match ${VAR_NAME} or ${VAR_NAME:default_value}
        pattern = r'\$\{([^}:]+)(?::([^}]*))?\}'
        
        def replace_var(match):
            var_name = match.group(1)
            default_value = match.group(2) if match.group(2) is not None else ""
            return os.environ.get(var_name, default_value)
        
        return re.sub(pattern, replace_var, value)
    
    elif isinstance(value, dict):
        return {k: substitute_env_vars(v) for k, v in value.items()}
    
    elif isinstance(value, list):
        return [substitute_env_vars(item) for item in value]
    
    else:
        return value


def load_config() -> Dict[str, Any]:
    """
    Load configuration from ~/.xerus/config.json with environment variable substitution.
    Also loads .env file if present in the config directory.
    """
    config_dir = Path.home() / '.xerus'
    config_file = config_dir / 'config.json'
    env_file = config_dir / '.env'
    
    # Load .env file if it exists and dotenv is available
    if DOTENV_AVAILABLE and env_file.exists():
        load_dotenv(env_file)
        console.print(f"[blue]Loaded environment variables from {env_file}[/blue]")
    elif env_file.exists() and not DOTENV_AVAILABLE:
        console.print(f"[yellow]Warning: .env file found at {env_file} but python-dotenv not installed[/yellow]")
        console.print("[yellow]Install with: uv add python-dotenv or pip install python-dotenv[/yellow]")
    
    if not config_file.exists():
        console.print(f"[red]Configuration file not found: {config_file}[/red]")
        console.print("[yellow]Run 'xerus init' to create a default configuration[/yellow]")
        return {}
    
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        # Perform environment variable substitution
        config = substitute_env_vars(config)
        
        return config
    except json.JSONDecodeError as e:
        console.print(f"[red]Error parsing configuration file: {e}[/red]")
        return {}
    except Exception as e:
        console.print(f"[red]Error loading configuration: {e}[/red]")
        return {} 