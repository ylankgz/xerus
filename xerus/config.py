import os
import json
import pkg_resources
from typing import Dict, Any

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
            # Try to get the template from package resources
            template_content = pkg_resources.resource_string(__name__, 'config_template.json').decode('utf-8')
            with open(config_path, 'w') as f:
                f.write(template_content)
            console.print(f"[green]Created default config file: {config_path}[/green]")
            console.print("[yellow]You can customize tool settings by editing this file[/yellow]")
        except Exception as e:
            console.print(f"[red]Error creating config file: {e}[/red]")
            console.print("[yellow]Continuing with default hardcoded settings[/yellow]")


def load_config() -> Dict[str, Any]:
    """Load configuration from ~/.xerus/config.json"""
    # Ensure config exists first
    ensure_config_exists()
    
    config_path = os.path.expanduser("~/.xerus/config.json")
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            # Expand environment variables in the config
            for tool_name, tool_config in config.get('tools', {}).items():
                for key, value in tool_config.items():
                    if isinstance(value, str) and value and value.startswith('${') and value.endswith('}'):
                        env_var = value[2:-1]  # Remove ${ and }
                        tool_config[key] = os.environ.get(env_var, value)
            return config
        except Exception as e:
            console.print(f"[red]Error loading config: {e}[/red]")
            return {}
    else:
        console.print(f"[yellow]Config file not found at {config_path}[/yellow]")
        return {} 