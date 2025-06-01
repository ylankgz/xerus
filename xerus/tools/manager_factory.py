from typing import List, Dict, Any
from smolagents import CodeAgent, LogLevel, ToolCallingAgent

from ..ui.display import console
from ..config import load_config
from ..model import ModelFactory
from .builtin_manager import BuiltInToolsManager
from .mcp_manager import MCPServerManager


class ManagerAgentFactory:
    """Factory class for creating manager agents with all configured tools."""
    
    def __init__(self):
        self.builtin_manager = BuiltInToolsManager()
        self.mcp_manager = MCPServerManager()
    
    def create_manager_agent(self, **kwargs) -> CodeAgent:
        """
        Setup and return manager agent from config.
        
        Args:
            **kwargs: Additional keyword arguments to pass to model creation
                     (e.g., temperature, top_p, max_tokens, etc.)
                     
        Returns:
            Configured CodeAgent instance
            
        Raises:
            ValueError: If manager agent configuration is missing
        """
        config = load_config()
        
        # Get manager agent config
        manager_config = config.get('manager_agent', {})
        
        if not manager_config:
            console.print("[red]Error: No manager_agent configuration found in config file[/red]")
            console.print("[yellow]Please ensure ~/.xerus/config.json contains a [manager_agent] section[/yellow]")
            raise ValueError("Manager agent configuration missing")
        
        # Get all tool agents
        all_tool_agents = self._setup_all_tool_agents(config, manager_config)
        
        # Create the model client with additional kwargs
        try:
            client = ModelFactory.create_client(
                model_id=manager_config.get("model_id"),
                api_key=manager_config.get("api_key"),
                api_base=manager_config.get("api_base"),
                **kwargs  # Pass through additional kwargs
            )
        except Exception as e:
            console.print(f"[red]Error creating manager agent model client: {e}[/red]")
            raise
        
        # Get manager agent parameters
        manager_params = manager_config.get("parameters", {})
        
        # Convert verbosity_level to LogLevel if it's an integer
        verbosity_level = manager_params.get("verbosity_level", 2)
        if isinstance(verbosity_level, int):
            verbosity_level = LogLevel(verbosity_level)
        
        # Create manager agent
        try:
            if manager_config.get("code_agent", True):
                manager_agent = CodeAgent(
                    tools=[],
                    model=client,
                    managed_agents=all_tool_agents,
                    additional_authorized_imports=manager_params.get("additional_authorized_imports", []),
                    max_steps=manager_params.get("max_steps", 10),
                    verbosity_level=verbosity_level,
                    name=manager_config.get("name"),
                    description=manager_config.get("description"),
                    stream_outputs=manager_params.get("stream_outputs", True),
                    use_structured_outputs_internally=manager_params.get("use_structured_outputs_internally", True)
                )
            else:
                manager_agent = ToolCallingAgent(
                    tools=[],
                    model=client,
                    managed_agents=all_tool_agents,
                    name=manager_config.get("name"),
                    description=manager_config.get("description"),
                )

            console.print(f"[green]Manager agent '{manager_config.get('name', 'unnamed')}' created successfully[/green]")
            return manager_agent
            
        except Exception as e:
            console.print(f"[red]Error creating manager agent: {e}[/red]")
            raise
    
    def _setup_all_tool_agents(self, config: Dict[str, Any], manager_config: Dict[str, Any]) -> List[CodeAgent]:
        """
        Setup all tool agents (built-in and MCP).
        
        Args:
            config: Full configuration dictionary
            manager_config: Manager agent configuration
            
        Returns:
            List of all configured tool agents
        """
        all_tool_agents = []
        
        # Setup built-in tool agents
        built_in_tools = self.builtin_manager.load_tools_from_config(config)
        built_in_agents = self.builtin_manager.create_tool_agents(built_in_tools)
        all_tool_agents.extend(built_in_agents)
        
        # Setup MCP tool agents if configured
        mcp_servers_config = config.get('mcpServers', {})
        if mcp_servers_config:
            console.print(f"[blue]Found {len(mcp_servers_config)} MCP server(s) in configuration[/blue]")
            
            # Set MCP server configurations
            self.mcp_manager.set_server_configs(mcp_servers_config)
            
            # Get default model config for MCP tools (use manager agent config as default)
            default_model_config = {
                "model_id": manager_config.get("model_id"),
                "api_key": manager_config.get("api_key"),
                "api_base": manager_config.get("api_base")
            }
            
            # Load MCP tools
            mcp_tools = self.mcp_manager.load_tools_from_servers()
            if mcp_tools:
                console.print(f"[green]Successfully loaded {len(mcp_tools)} MCP tools[/green]")
                
                # Convert MCP tools to tool agents
                mcp_tool_agents = self.mcp_manager.create_tool_agents(mcp_tools, default_model_config)
                all_tool_agents.extend(mcp_tool_agents)
                
                console.print(f"[green]Added {len(mcp_tool_agents)} MCP tool agents[/green]")
            else:
                console.print("[yellow]No MCP tools were loaded[/yellow]")
        
        return all_tool_agents 