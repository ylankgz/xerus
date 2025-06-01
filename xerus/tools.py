import importlib.util
import os
from typing import List, Optional

from smolagents import Tool, CodeAgent, LogLevel, ToolCollection

from .ui.display import console
from .model import ModelFactory
from .errors import AgentRuntimeError
from .config import load_config
from mcp import StdioServerParameters

def create_tool_agent(
    model_id,
    api_key,
    api_base,
    tools: List[Tool],
    name: Optional[str] = None,
    description: Optional[str] = None,
    **kwargs
)-> CodeAgent:
    """
    Create a tool agent with specified model and tool.
    
    Args:
        model_id: ID or name of the model
        api_key: API key for the model service
        tool: Tool instance
        api_base: The base URL of the API server (for OpenAI and similar APIs)
        name: Optional agent name for uniqueness
        description: Optional description of the agent
    Returns:
        The initialized CodeAgent

    Raises:
        AgentRuntimeError: For other agent setup errors
    """

    tool_model = ModelFactory.create_client(
        model_id=model_id,
        api_key=api_key,
        api_base=api_base,
        **kwargs
    )

    # Initialize the tool agent
    try:
        agent = CodeAgent(
            tools=tools,
            model=tool_model,
            name=name,
            description=description,
            stream_outputs=True,
            use_structured_outputs_internally=True,
            **kwargs
        )
        return agent
    except Exception as e:
        raise AgentRuntimeError(
            f"Failed to initialize tool agent: {e}",
            "Check model configuration and tool compatibility for tool: {tool}"
        )

def import_tool_class(tool_class_path: str):
    """Dynamically import a tool class from its module path."""
    try:
        module_path, class_name = tool_class_path.rsplit('.', 1)
        module = importlib.import_module(module_path)
        tool_class = getattr(module, class_name)
        return tool_class
    except (ImportError, AttributeError, ValueError) as e:
        console.print(f"[red]Error importing tool class '{tool_class_path}': {e}[/red]")
        return None

def create_mcp_server_parameters(mcp_config: dict) -> Optional[StdioServerParameters]:
    """Convert Claude Desktop MCP config format to StdioServerParameters."""
    if StdioServerParameters is None:
        console.print("[red]Error: mcp package not available for MCP server creation[/red]")
        return None
    
    try:
        command = mcp_config.get("command")
        args = mcp_config.get("args", [])
        env = mcp_config.get("env", {})
        
        if not command:
            console.print("[red]Error: MCP server config missing 'command' field[/red]")
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
        console.print(f"[red]Error creating MCP server parameters: {e}[/red]")
        return None

def load_mcp_tools(mcp_servers_config: dict) -> List[Tool]:
    """Load all tools from configured MCP servers."""
    all_mcp_tools = []
    
    if not mcp_servers_config:
        return all_mcp_tools
    
    for server_name, server_config in mcp_servers_config.items():
        # Skip servers that start with underscore (comments) or are disabled
        if server_name.startswith('_') or server_config.get('_disabled', False):
            console.print(f"[yellow]Skipping disabled MCP server: {server_name}[/yellow]")
            continue
            
        console.print(f"[blue]Loading MCP server: {server_name}[/blue]")
        
        # Create server parameters
        server_params = create_mcp_server_parameters(server_config)
        if not server_params:
            console.print(f"[red]Failed to create server parameters for {server_name}[/red]")
            continue
        
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
            console.print(f"[yellow]Make sure the MCP server package is installed and configured correctly[/yellow]")
            continue
    
    return all_mcp_tools

def setup_mcp_tool_agents(mcp_tools: List[Tool], mcp_servers_config: dict, default_model_config: dict) -> List[CodeAgent]:
    """Convert MCP tools into tool agents with individual model configurations."""
    mcp_tool_agents = []
    
    for tool in mcp_tools:
        try:
            # Extract server name from tool name (format: server_name_tool_name)
            server_name = tool.name.split('_')[0] if '_' in tool.name else 'unknown'
            
            # Get server-specific model configuration
            server_config = mcp_servers_config.get(server_name, {})
            model_config = {
                "model_id": server_config.get("model_id", default_model_config.get("model_id")),
                "api_key": server_config.get("api_key", default_model_config.get("api_key")),
                "api_base": server_config.get("api_base", default_model_config.get("api_base"))
            }
            
            # Create agent with server-specific or default model configuration
            agent = create_tool_agent(
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

def setup_built_in_tools():
    """Setup and return built-in tools as agent list."""
    # Load config from JSON file
    config = load_config()

    tools = []
    tool_configs = config.get('tools', {})
    
    for tool_name, tool_config in tool_configs.items():
        # Get tool class path from config
        tool_class_path = tool_config.get("tool_class")
        if not tool_class_path:
            console.print(f"[yellow]Warning: No tool_class specified for {tool_name}, skipping[/yellow]")
            continue
        
        # Dynamically import the tool class
        tool_class = import_tool_class(tool_class_path)
        if not tool_class:
            console.print(f"[yellow]Warning: Could not load tool class for {tool_name}, skipping[/yellow]")
            continue
        
        # Get tool parameters from config
        tool_params = tool_config.get("parameters", {})
        
        # Create tool instance with parameters using universal approach
        try:
            tool_instance = tool_class(**tool_params)
        except TypeError as e:
            # If tool doesn't accept the parameters, try without them
            console.print(f"[yellow]Warning: Tool {tool_name} doesn't accept some parameters: {e}[/yellow]")
            console.print(f"[yellow]Creating {tool_name} without parameters[/yellow]")
            try:
                tool_instance = tool_class()
            except Exception as e2:
                console.print(f"[red]Error creating tool {tool_name}: {e2}[/red]")
                continue
        
        tools.append({
            "tool": tool_instance,
            "name": tool_config.get("name", tool_name),
            "description": tool_config.get("description", ""),
            "model_id": tool_config.get("model_id", ""),
            "api_key": tool_config.get("api_key", ""),
            "api_base": tool_config.get("api_base", "")
        })

    built_in_tools_agents_list = []

    for tool in tools:
        built_in_tools_agents_list.append(
            create_tool_agent(
                tool["model_id"],
                tool["api_key"],
                tool["api_base"],
                [tool["tool"]],
                name=tool["name"],
                description=tool["description"]
            )
        )

    # Load MCP tools if configured
    mcp_servers_config = config.get('mcpServers', {})
    if mcp_servers_config:
        console.print(f"[blue]Found {len(mcp_servers_config)} MCP server(s) in configuration[/blue]")
        
        # Get default model config for MCP tools (use manager agent config as default)
        manager_config = config.get('manager_agent', {})
        default_model_config = {
            "model_id": manager_config.get("model_id"),
            "api_key": manager_config.get("api_key"),
            "api_base": manager_config.get("api_base")
        }
        
        # Load MCP tools
        mcp_tools = load_mcp_tools(mcp_servers_config)
        if mcp_tools:
            console.print(f"[green]Successfully loaded {len(mcp_tools)} MCP tools[/green]")
            
            # Convert MCP tools to tool agents
            mcp_tool_agents = setup_mcp_tool_agents(mcp_tools, mcp_servers_config, default_model_config)
            built_in_tools_agents_list.extend(mcp_tool_agents)
            
            console.print(f"[green]Added {len(mcp_tool_agents)} MCP tool agents[/green]")
        else:
            console.print("[yellow]No MCP tools were loaded[/yellow]")

    return built_in_tools_agents_list

def setup_manager_agent(**kwargs):
    """Setup and return manager agent from config.
    
    Args:
        **kwargs: Additional keyword arguments to pass to model creation
                 (e.g., temperature, top_p, max_tokens, etc.)
    """
    config = load_config()
    
    # Get manager agent config
    manager_config = config.get('manager_agent', {})
    
    if not manager_config:
        console.print("[red]Error: No manager_agent configuration found in config file[/red]")
        console.print("[yellow]Please ensure ~/.xerus/config.json contains a [manager_agent] section[/yellow]")
        raise ValueError("Manager agent configuration missing")
    
    # Get manager agent parameters
    manager_params = manager_config.get("parameters", {})
    
    # Get built-in tools
    built_in_tools_agents_list = setup_built_in_tools()
    
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
    
    # Convert verbosity_level to LogLevel if it's an integer
    verbosity_level = manager_params.get("verbosity_level", 2)
    if isinstance(verbosity_level, int):
        verbosity_level = LogLevel(verbosity_level)
    
    # Create manager agent
    try:
        manager_agent = CodeAgent(
            tools=[],
            model=client,
            managed_agents=built_in_tools_agents_list,
            additional_authorized_imports=manager_params.get("additional_authorized_imports", []),
            max_steps=manager_params.get("max_steps", 10),
            verbosity_level=verbosity_level,
            name=manager_config.get("name"),
            description=manager_config.get("description"),
            stream_outputs=manager_params.get("stream_outputs", True),
            use_structured_outputs_internally=manager_params.get("use_structured_outputs_internally", True)
        )
        
        console.print(f"[green]Manager agent '{manager_config.get('name', 'unnamed')}' created successfully[/green]")
        return manager_agent
        
    except Exception as e:
        console.print(f"[red]Error creating manager agent: {e}[/red]")
        raise

def list_mcp_tools():
    """List all available MCP tools from configuration (for debugging)."""
    config = load_config()
    mcp_servers_config = config.get('mcpServers', {})
    
    if not mcp_servers_config:
        console.print("[yellow]No MCP servers configured[/yellow]")
        return
    
    console.print("[blue]MCP Server Configuration:[/blue]")
    for server_name, server_config in mcp_servers_config.items():
        if server_name.startswith('_'):
            continue
            
        status = "disabled" if server_config.get('_disabled', False) else "enabled"
        command = server_config.get('command', 'N/A')
        console.print(f"  {server_name}: {status} (command: {command})")
    
    # Try to load tools
    console.print("\n[blue]Loading MCP tools...[/blue]")
    mcp_tools = load_mcp_tools(mcp_servers_config)
    
    if mcp_tools:
        console.print(f"\n[green]Found {len(mcp_tools)} MCP tools:[/green]")
        for tool in mcp_tools:
            console.print(f"  - {tool.name}: {getattr(tool, 'description', 'No description')}")
    else:
        console.print("[yellow]No MCP tools loaded[/yellow]")



