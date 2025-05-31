import os
import importlib.util
import pkg_resources
from typing import List, Optional, Dict, Any

from smolagents import Tool, CodeAgent, LogLevel

from .ui.display import console
from .model import ModelFactory
from .errors import AgentRuntimeError
from .config import load_config

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
