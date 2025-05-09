"""
Agent module for Xerus package.
"""
import importlib
import importlib.util
from typing import List, Optional

from rich.console import Console
from smolagents import CodeAgent

from .models import get_model
from .tools import ToolManager
from .errors import (
    ToolLoadError,
    ToolExecutionError,
    ModelInitializationError,
    AgentRuntimeError
)

console = Console()

def create_agent(model_type, model_id, api_key=None, tools=None, imports=None, 
               tool_local=None, tool_hub=None, tool_space=None, tool_collection=None,
               tool_dirs=None):
    """
    Create a CodeAgent with specified model and tools.
    
    Args:
        model_type: Type of model to use
        model_id: ID or name of the model
        api_key: API key for the model service
        tools: List of tool names or specifications to enable
        imports: List of Python packages to authorize for import
        tool_local: Path to a local tool file
        tool_hub: Hugging Face Hub repo ID for a tool
        tool_space: Hugging Face Space ID to import as a tool
        tool_collection: Hugging Face Hub repo ID for a collection of tools
        tool_dirs: List of directories to discover tools from
    
    Returns:
        The initialized CodeAgent
        
    Raises:
        ModelInitializationError: If model initialization fails
        ToolLoadError: If a tool fails to load
        AgentRuntimeError: For other agent setup errors
    """
    model = get_model(model_type, model_id, api_key)
    
    # Initialize the tool manager
    tool_manager = ToolManager()
    available_tools = []
    
    # Process tool specifications
    if tools:
        for tool_spec in tools:
            try:
                loaded_tools = tool_manager.load_tool_from_spec(tool_spec)
                if isinstance(loaded_tools, list):
                    available_tools.extend(loaded_tools)
                else:
                    available_tools.append(loaded_tools)
            except ToolLoadError as e:
                console.print(f"[yellow]Warning: Failed to load tool '{tool_spec}': {e}[/yellow]")
    
    # Load tools from additional sources
    if tool_local:
        try:
            local_tools = tool_manager.load_from_local_file(tool_local)
            available_tools.extend(local_tools)
        except ToolLoadError as e:
            raise ToolLoadError(str(e))
    
    if tool_hub:
        try:
            hub_tool = tool_manager.load_from_hub(tool_hub)
            available_tools.append(hub_tool)
        except ToolLoadError as e:
            raise ToolLoadError(str(e))
    
    if tool_space:
        try:
            # Extract name and description if provided in format "space_id:name:description"
            parts = tool_space.split(":", 2)
            space_id = parts[0]
            name = parts[1] if len(parts) > 1 else None
            description = parts[2] if len(parts) > 2 else None
            
            space_tool = tool_manager.load_from_space(space_id, name, description)
            available_tools.append(space_tool)
        except ToolLoadError as e:
            raise ToolLoadError(str(e))
    
    if tool_collection:
        try:
            collection_tools = tool_manager.load_from_collection(tool_collection)
            available_tools.extend(collection_tools)
        except ToolLoadError as e:
            raise ToolLoadError(str(e))
    
    # Discover tools from directories
    if tool_dirs:
        for directory in tool_dirs:
            try:
                discovered_tools = tool_manager.discover_tools(directory)
                available_tools.extend(discovered_tools)
                console.print(f"[green]Discovered {len(discovered_tools)} tools in {directory}[/green]")
            except Exception as e:
                console.print(f"[yellow]Warning: Error discovering tools in {directory}: {e}[/yellow]")
    
    # Get unique tools based on name
    unique_tools = {}
    for tool in available_tools:
        unique_tools[tool.name] = tool
    
    additional_imports = []
    if imports:
        additional_imports.extend(imports.split())
    
    try:
        return CodeAgent(
            tools=list(unique_tools.values()),
            model=model, 
            additional_authorized_imports=additional_imports
        )
    except Exception as e:
        raise AgentRuntimeError(
            f"Failed to initialize agent: {e}",
            "Check model configuration and tool compatibility"
        ) 