#!/usr/bin/env python3
"""
Example script demonstrating MCP (Model Context Protocol) integration with Xerus.

This script shows how to:
1. Configure MCP servers in the config.json
2. Load MCP tools
3. Use MCP tools with Xerus agents

Prerequisites:
- Install the mcp package: pip install mcp
- Install desired MCP server packages (e.g., uvx mcp-server-appwrite)
- Configure your MCP servers in ~/.xerus/config.json
"""

import sys
import os

# Add xerus to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from xerus.tools import list_mcp_tools, setup_manager_agent
from xerus.ui.display import console

def main():
    """Main example function."""
    console.print("[bold blue]Xerus MCP Tools Example[/bold blue]")
    console.print("=" * 50)
    
    # List configured MCP tools
    console.print("\n[bold]1. Listing MCP Tools:[/bold]")
    list_mcp_tools()
    
    # Example of using MCP tools with manager agent
    console.print("\n[bold]2. Setting up Manager Agent with MCP Tools:[/bold]")
    try:
        manager_agent = setup_manager_agent()
        
        # Get managed agents (includes MCP tools)
        managed_agents = manager_agent.managed_agents
        mcp_agents = [agent for agent in managed_agents if hasattr(agent, 'name') and agent.name.startswith('mcp_')]
        
        console.print(f"[green]Manager agent created with {len(managed_agents)} total tools[/green]")
        console.print(f"[green]Including {len(mcp_agents)} MCP tool agents[/green]")
        
        if mcp_agents:
            console.print("\n[bold]MCP Tool Agents:[/bold]")
            for agent in mcp_agents:
                console.print(f"  - {agent.name}: {getattr(agent, 'description', 'No description')}")
        
        # Example usage (uncomment to test with actual query)
        # console.print("\n[bold]3. Example Query:[/bold]")
        # result = manager_agent.run("List available tools and their capabilities")
        # console.print(f"Result: {result}")
        
    except Exception as e:
        console.print(f"[red]Error setting up manager agent: {e}[/red]")

def example_config():
    """Show example MCP server configuration."""
    console.print("\n[bold]Example MCP Server Configuration for ~/.xerus/config.json:[/bold]")
    
    example_config = '''
{
  "mcpServers": {
    "appwrite": {
      "command": "uvx",
      "args": ["mcp-server-appwrite"],
      "env": {
        "APPWRITE_PROJECT_ID": "${APPWRITE_PROJECT_ID}",
        "APPWRITE_API_KEY": "${APPWRITE_API_KEY}",
        "APPWRITE_ENDPOINT": "${APPWRITE_ENDPOINT:https://cloud.appwrite.io/v1}"
      },
      "model_id": "openai/meta-llama/Llama-4-Scout-17B-16E-Instruct",
      "api_key": "${GMI_CLOUD_API_KEY}",
      "api_base": "https://api.gmi-serving.com/v1"
    },
    "filesystem": {
      "command": "uvx",
      "args": ["mcp-server-filesystem", "${FILESYSTEM_ROOT_PATH:/tmp/allowed}"],
      "model_id": "openai/deepseek-ai/DeepSeek-R1-0528",
      "api_key": "${GMI_CLOUD_API_KEY}",
      "api_base": "https://api.gmi-serving.com/v1"
    },
    "github": {
      "command": "uvx", 
      "args": ["mcp-server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
      },
      "model_id": "openai/meta-llama/Llama-4-Scout-17B-16E-Instruct",
      "api_key": "${GMI_CLOUD_API_KEY}",
      "api_base": "https://api.gmi-serving.com/v1"
    }
  }
}
'''
    
    console.print(example_config)
    
    console.print("\n[bold]Example ~/.xerus/.env file:[/bold]")
    
    example_env = '''
# Xerus Environment Variables
# Copy to ~/.xerus/.env and set your actual values

# API Configuration
GMI_CLOUD_API_KEY=your_gmi_cloud_api_key_here

# Appwrite MCP Server
APPWRITE_PROJECT_ID=your_appwrite_project_id
APPWRITE_API_KEY=your_appwrite_api_key
APPWRITE_ENDPOINT=https://cloud.appwrite.io/v1

# GitHub MCP Server
GITHUB_TOKEN=your_github_personal_access_token

# Filesystem MCP Server
FILESYSTEM_ROOT_PATH=/path/to/allowed/directory

# Database MCP Servers
SQLITE_DB_PATH=/path/to/your/database.db
'''
    
    console.print(example_env)
    
    console.print("\n[bold]Available MCP Servers:[/bold]")
    console.print("- mcp-server-appwrite: Appwrite backend integration")
    console.print("- mcp-server-filesystem: File system access")
    console.print("- mcp-server-github: GitHub API integration")
    console.print("- mcp-server-sqlite: SQLite database tools")
    console.print("- mcp-server-memory: Memory/knowledge base tools")
    
    console.print("\n[bold]Environment Variable Features:[/bold]")
    console.print("- ${VAR_NAME} - Required variable")
    console.print("- ${VAR_NAME:default_value} - Variable with default value")
    console.print("- Load variables from ~/.xerus/.env file")
    console.print("- Individual model configuration per MCP server")
    
    console.print("\n[bold]Installation:[/bold]")
    console.print("pip install mcp python-dotenv")
    console.print("uvx --help  # Install uvx if needed")

if __name__ == "__main__":
    try:
        main()
        example_config()
    except KeyboardInterrupt:
        console.print("\n[yellow]Example interrupted by user[/yellow]")
    except Exception as e:
        console.print(f"\n[red]Error running example: {e}[/red]") 