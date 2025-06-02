import os
import shutil
import stat
from pathlib import Path
from typing import Optional
import rich_click as click

from ..error_handler import handle_command_errors
from ..ui.display import console

PROVIDERS = {
    "openai": {
        "name": "OpenAI",
        "description": "OpenAI - Advanced AI models",
        "api_key_env": "OPENAI_API_KEY",
        "config_template": "config_template_openai.json",
        "api_base": "https://api.openai.com/v1",
        "website": "https://platform.openai.com/"
    },
    "nebius": {
        "name": "Nebius",
        "description": "Nebius AI Studio - High-performance cloud AI platform",
        "api_key_env": "NEBIUS_API_KEY",
        "config_template": "config_template_nebius.json",
        "api_base": "https://api.studio.nebius.com/v1/",
        "website": "https://studio.nebius.com/"
    },
    "novita": {
        "name": "Novita",
        "description": "Novita AI - Affordable AI inference platform",
        "api_key_env": "NOVITA_API_KEY", 
        "config_template": "config_template_novita.json",
        "api_base": "https://api.novita.ai/v3/openai",
        "website": "https://novita.ai/"
    },
    "gmi_cloud": {
        "name": "GMI Cloud",
        "description": "GMI Cloud - High Performance GPU Cloud Solutions",
        "api_key_env": "GMI_CLOUD_API_KEY", 
        "config_template": "config_template_gmi.json",
        "api_base": "https://api.gmi-serving.com/v1",
        "website": "https://www.gmicloud.ai/"
    },
}

@click.command()
@click.option("--provider", 
              type=click.Choice(list(PROVIDERS.keys())), 
              help="Choose AI provider")
@click.option("--api-key", 
              help="API key for the selected provider (will prompt if not provided)")
@click.option("--force", "-f", 
              is_flag=True, 
              help="Force overwrite existing configuration")
@handle_command_errors
def init(provider: Optional[str], api_key: Optional[str], force: bool):
    """[bold]Initialize Xerus configuration[/bold] with AI provider setup.
    
    Creates ~/.xerus directory with config.json and .env files for your chosen provider.
    
    Examples:\n
    [green]xerus init[/green] - Interactive provider selection and API key input\n
    [green]xerus init --provider nebius[/green] - Use Nebius provider, prompt for API key\n
    [green]xerus init --provider novita --api-key YOUR_KEY[/green] - Use Novita with provided API key\n
    [green]xerus init --provider novita --force[/green] - Use Novita and overwrite existing config\n
    """
    
    xerus_dir = Path.home() / '.xerus'
    config_file = xerus_dir / 'config.json'
    env_file = xerus_dir / '.env'
    
    # Check if already initialized
    if config_file.exists() and not force:
        console.print(f"[yellow]Xerus is already initialized at {xerus_dir}[/yellow]")
        console.print("[green]Use --force to overwrite existing configuration[/green]")
        console.print(f"[blue]Current config: {config_file}[/blue]")
        return
    
    # Create xerus directory
    xerus_dir.mkdir(exist_ok=True)
    console.print(f"[green]Created directory: {xerus_dir}[/green]")
    
    # Provider selection
    if not provider:
        console.print("\n[bold]Available AI Providers:[/bold]\n")
        
        for key, info in PROVIDERS.items():
            console.print(f"[bold cyan]{key}[/bold cyan] - {info['name']}")
            console.print(f"  {info['description']}")
            console.print(f"  API Base: {info['api_base']}")
            console.print(f"  Website: {info['website']}")
            console.print()
        
        provider = click.prompt(
            "Select provider", 
            type=click.Choice(list(PROVIDERS.keys())),
            show_choices=True
        )
    
    provider_info = PROVIDERS[provider]
    console.print(f"\n[bold green]Initializing with {provider_info['name']}[/bold green]")
    
    # Copy appropriate config template
    template_path = Path(__file__).parent.parent / 'config_templates' / provider_info['config_template']
    
    if not template_path.exists():
        console.print(f"[red]Error: Template not found: {template_path}[/red]")
        return
    
    shutil.copy2(template_path, config_file)
    console.print(f"[green]Created config file: {config_file}[/green]")
    
    # API key handling
    if not api_key:
        console.print(f"\n[bold blue]API Key Setup[/bold blue]")
        console.print(f"To use {provider_info['name']}, you need an API key from: [link]{provider_info['website']}[/link]")
        
        # Check if API key already exists in environment
        existing_api_key = os.environ.get(provider_info['api_key_env'], "")
        if existing_api_key:
            console.print(f"[yellow]Found existing {provider_info['api_key_env']} in environment[/yellow]")
            use_existing = click.confirm(
                f"Use existing API key from environment?",
                default=True
            )
            if use_existing:
                api_key = existing_api_key
                console.print(f"[green]✓ Using existing API key from environment[/green]")
            else:
                api_key = click.prompt(
                    f"Enter your {provider_info['name']} API key",
                    hide_input=True
                )
        else:
            api_key = click.prompt(
                f"Enter your {provider_info['name']} API key",
                hide_input=True
            )
    
    # Validate API key is not empty
    if not api_key or api_key.strip() == "":
        console.print("[red]Error: API key cannot be empty[/red]")
        return
    
    # Create .env file with the API key
    env_content = f"""# Xerus Environment Configuration for {provider_info['name']}
# API key for {provider_info['name']}
{provider_info['api_key_env']}={api_key.strip()}

# Optional: Add other environment variables here
# GITHUB_TOKEN=your_github_token_here
"""
    
    with open(env_file, 'w') as f:
        f.write(env_content)
    
    # Set secure permissions on .env file (owner read/write only)
    try:
        os.chmod(env_file, stat.S_IRUSR | stat.S_IWUSR)  # 600 permissions
        console.print(f"[green]Created environment file: {env_file} (permissions: 600)[/green]")
    except OSError as e:
        console.print(f"[green]Created environment file: {env_file}[/green]")
        console.print(f"[yellow]Warning: Could not set secure permissions: {e}[/yellow]")
    
    console.print(f"[green]✓ API key configured for {provider_info['name']}[/green]")
    
    # Instructions
    console.print(f"\n[bold blue]Setup Complete![/bold blue]")
    console.print(f"[green]✓ Configuration files created[/green]")
    console.print(f"[green]✓ API key configured with secure permissions[/green]")
    console.print(f"\n[bold blue]Next Steps:[/bold blue]")
    console.print(f"1. Customize your configuration (optional): [cyan]{config_file}[/cyan]")
    console.print(f"2. Start using Xerus: [green]xerus run --prompt \"Hello world\"[/green]")
    console.print(f"3. Start interactive chat: [green]xerus chat[/green]")
    
    console.print(f"\n[bold green]Xerus initialized successfully with {provider_info['name']}![/bold green]") 