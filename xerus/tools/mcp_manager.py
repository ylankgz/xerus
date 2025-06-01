import os
from typing import Dict, List, Optional, Union
from smolagents import Tool, CodeAgent, ToolCollection

from ..ui.display import console
from .factory import ToolAgentFactory

from mcp import StdioServerParameters


class MCPServerManager:
    """Manages MCP server operations including loading tools and creating agents."""
    
    def __init__(self):
        self.server_configs: Dict[str, dict] = {}
    
    def set_server_configs(self, mcp_servers_config: Dict[str, dict]) -> None:
        """Set the MCP server configurations."""
        self.server_configs = mcp_servers_config or {}
    
    def create_server_config(self, mcp_config: dict) -> Optional[Union[StdioServerParameters, dict]]:
        """
        Create MCP server configuration for either stdio or HTTP-based servers.
        
        Args:
            mcp_config: Server configuration dictionary
            
        Returns:
            Server configuration object or None if creation failed
        """
        try:
            # Check if this is an HTTP-based server
            if mcp_config.get("transport") == "streamable-http":
                url = mcp_config.get("url")
                if not url:
                    console.print("[red]Error: HTTP-based MCP server config missing 'url' field[/red]")
                    return None
                
                return {
                    "url": url,
                    "transport": "streamable-http"
                }
            
            command = mcp_config.get("command")
            args = mcp_config.get("args", [])
            env = mcp_config.get("env", {})
            
            if not command:
                console.print("[red]Error: stdio-based MCP server config missing 'command' field[/red]")
                return None
            
            # Merge environment variables with current environment
            merged_env = {**os.environ, **env}
            
            server_params = StdioServerParameters(
                command=command,
                args=args,
                env=merged_env
            )
            
            return server_params
            
        except Exception as e:
            console.print(f"[red]Error creating MCP server configuration: {e}[/red]")
            return None
    
    def load_tools_from_servers(self) -> List[Tool]:
        """
        Load all tools from configured MCP servers.
        
        Returns:
            List of loaded MCP tools
        """
        all_mcp_tools = []
        
        if not self.server_configs:
            return all_mcp_tools
        
        for server_name, server_config in self.server_configs.items():
            # Skip servers that start with underscore (comments) or are disabled
            if server_name.startswith('_') or server_config.get('_disabled', False):
                console.print(f"[yellow]Skipping disabled MCP server: {server_name}[/yellow]")
                continue
                
            console.print(f"[blue]Loading MCP server: {server_name}[/blue]")
            
            # Create server configuration (supports both stdio and HTTP)
            server_params = self.create_server_config(server_config)
            if not server_params:
                console.print(f"[red]Failed to create server configuration for {server_name}[/red]")
                continue
            
            # Determine server type for logging
            server_type = "HTTP-based" if isinstance(server_params, dict) and server_params.get("transport") == "streamable-http" else "stdio-based"
            console.print(f"[blue]Connecting to {server_type} MCP server: {server_name}[/blue]")
            
            try:
                # Load tools from MCP server using ToolCollection
                with ToolCollection.from_mcp(server_params, trust_remote_code=True) as tool_collection:
                    tools = tool_collection.tools
                    console.print(f"[green]Loaded {len(tools)} tools from MCP server '{server_name}'[/green]")
                    
                    # Add server name as prefix to tool names for identification
                    for tool in tools:
                        # Store original name and add server prefix
                        original_name = getattr(tool, 'name', tool.__class__.__name__)
                        tool.name = f"{server_name}_{original_name}"
                        all_mcp_tools.append(tool)
                        
            except Exception as e:
                console.print(f"[red]Error loading tools from MCP server '{server_name}': {e}[/red]")
                if server_type == "stdio-based":
                    console.print(f"[yellow]Make sure the MCP server package is installed and configured correctly[/yellow]")
                else:
                    console.print(f"[yellow]Make sure the HTTP MCP server is running and accessible at the configured URL[/yellow]")
                continue
        
        return all_mcp_tools
    
    def create_tool_agents(self, mcp_tools: List[Tool], default_model_config: dict) -> List[CodeAgent]:
        """
        Convert MCP tools into tool agents with individual model configurations.
        
        Args:
            mcp_tools: List of MCP tools to convert
            default_model_config: Default model configuration to use
            
        Returns:
            List of created CodeAgent instances
        """
        mcp_tool_agents = []
        
        for tool in mcp_tools:
            try:
                # Extract server name from tool name (format: server_name_tool_name)
                server_name = tool.name.split('_')[0] if '_' in tool.name else 'unknown'
                
                # Get server-specific model configuration
                server_config = self.server_configs.get(server_name, {})
                model_config = {
                    "model_id": server_config.get("model_id", default_model_config.get("model_id")),
                    "api_key": server_config.get("api_key", default_model_config.get("api_key")),
                    "api_base": server_config.get("api_base", default_model_config.get("api_base"))
                }
                
                # Create agent with server-specific or default model configuration
                agent = ToolAgentFactory.create_agent(
                    model_id=model_config["model_id"],
                    api_key=model_config["api_key"],
                    api_base=model_config["api_base"],
                    tools=[tool],
                    name=f"mcp_{tool.name}",
                    description=getattr(tool, 'description', f"MCP tool: {tool.name}")
                )
                mcp_tool_agents.append(agent)
                
                # Log which model configuration was used
                model_display = model_config["model_id"] or "default"
                console.print(f"[green]Created MCP agent '{tool.name}' using model: {model_display}[/green]")
                
            except Exception as e:
                console.print(f"[red]Error creating agent for MCP tool '{tool.name}': {e}[/red]")
                continue
        
        return mcp_tool_agents
    
    def list_tools(self) -> None:
        """List all available MCP tools from configuration (for debugging)."""
        if not self.server_configs:
            console.print("[yellow]No MCP servers configured[/yellow]")
            return
        
        console.print("[blue]MCP Server Configuration:[/blue]")
        for server_name, server_config in self.server_configs.items():
            if server_name.startswith('_'):
                continue
                
            status = "disabled" if server_config.get('_disabled', False) else "enabled"
            
            # Determine server type and show relevant info
            if server_config.get("transport") == "streamable-http":
                server_type = "HTTP"
                connection_info = server_config.get('url', 'N/A')
            else:
                server_type = "stdio"
                connection_info = server_config.get('command', 'N/A')
            
            console.print(f"  {server_name}: {status} ({server_type}: {connection_info})")
        
        # Try to load tools
        console.print("\n[blue]Loading MCP tools...[/blue]")
        mcp_tools = self.load_tools_from_servers()
        
        if mcp_tools:
            console.print(f"\n[green]Found {len(mcp_tools)} MCP tools:[/green]")
            for tool in mcp_tools:
                console.print(f"  - {tool.name}: {getattr(tool, 'description', 'No description')}")
        else:
            console.print("[yellow]No MCP tools loaded[/yellow]") 