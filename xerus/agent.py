"""
Agent module for Xerus package.
"""
import importlib
import importlib.util
from typing import List, Optional

from rich.console import Console
from smolagents import CodeAgent
from smolagents import WebSearchTool
from smolagents import Tool, load_tool, ToolCollection

from .models import get_model
from .errors import (
    ToolLoadError,
    ToolExecutionError,
    ModelInitializationError,
    AgentRuntimeError
)

console = Console()

def create_agent(model_type, model_id, api_key=None, tools=None, imports=None, 
               tool_local=None, tool_hub=None, tool_space=None, tool_collection=None):
    """
    Create a CodeAgent with specified model and tools.
    
    Args:
        model_type: Type of model to use
        model_id: ID or name of the model
        api_key: API key for the model service
        tools: List of tools to enable
        imports: List of Python packages to authorize for import
        tool_local: Path to a local tool file
        tool_hub: Hugging Face Hub repo ID for a tool
        tool_space: Hugging Face Space ID to import as a tool
        tool_collection: Hugging Face Hub repo ID for a collection of tools
    
    Returns:
        The initialized CodeAgent
        
    Raises:
        ModelInitializationError: If model initialization fails
        ToolLoadError: If a tool fails to load
        AgentRuntimeError: For other agent setup errors
    """
    model = get_model(model_type, model_id, api_key)
    
    available_tools = []
    if tools:
        if "web_search" in tools:
            try:
                available_tools.append(WebSearchTool())
                console.print("[green]Successfully enabled web search tool[/green]")
            except Exception as e:
                raise ToolLoadError(
                    f"Failed to initialize web search tool: {e}",
                    "Check your internet connection and try again"
                )
    
    # Add tool from local file if specified
    if tool_local:
        try:
            console.print(f"[bold blue]Loading tool from local file: {tool_local}[/bold blue]")
            # Import the module dynamically
            spec = importlib.util.spec_from_file_location("local_tool", tool_local)
            if not spec:
                raise ToolLoadError(
                    f"Could not load spec from file: {tool_local}",
                    "Ensure the file exists and is a valid Python module"
                )
                
            local_tool_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(local_tool_module)
            
            # Find Tool instances in the module
            tools_found = False
            for name in dir(local_tool_module):
                obj = getattr(local_tool_module, name)
                if isinstance(obj, Tool):
                    available_tools.append(obj)
                    tools_found = True
                    console.print(f"[green]Successfully loaded tool: {obj.name}[/green]")
            
            if not tools_found:
                raise ToolLoadError(
                    f"No Tool instances found in {tool_local}",
                    "Ensure the file contains properly defined Tool instances"
                )
        except ToolLoadError:
            raise
        except Exception as e:
            raise ToolLoadError(f"Error loading tool from local file: {str(e)}")
    
    # Add tool from Hugging Face Hub if specified
    if tool_hub:
        try:
            console.print(f"[bold blue]Loading tool from Hugging Face Hub: {tool_hub}[/bold blue]")
            hub_tool = load_tool(tool_hub, trust_remote_code=True)
            available_tools.append(hub_tool)
            console.print(f"[green]Successfully loaded tool from Hub: {hub_tool.name}[/green]")
        except Exception as e:
            raise ToolLoadError(
                f"Error loading tool from Hub ({tool_hub}): {str(e)}",
                "Check that the tool exists and you have proper permissions"
            )
    
    # Add tool from Hugging Face Space if specified
    if tool_space:
        try:
            # Extract name and description if provided in format "space_id:name:description"
            parts = tool_space.split(":", 2)
            space_id = parts[0]
            name = parts[1] if len(parts) > 1 else "space_tool"
            description = parts[2] if len(parts) > 2 else f"Tool from Space {space_id}"
            
            console.print(f"[bold blue]Loading tool from Hugging Face Space: {space_id}[/bold blue]")
            space_tool = Tool.from_space(space_id, name=name, description=description)
            available_tools.append(space_tool)
            console.print(f"[green]Successfully loaded tool from Space: {name}[/green]")
        except Exception as e:
            raise ToolLoadError(
                f"Error loading tool from Space ({tool_space}): {str(e)}",
                "Check that the Space exists and is properly configured as a tool"
            )
    
    # Add tools from collection if specified
    if tool_collection:
        try:
            console.print(f"[bold blue]Loading tool collection from Hub: {tool_collection}[/bold blue]")
            collection = ToolCollection.from_hub(collection_slug=tool_collection, trust_remote_code=True)
            if not collection.tools:
                raise ToolLoadError(
                    f"No tools found in collection: {tool_collection}",
                    "Verify that the collection exists and contains valid tools"
                )
            # Add all tools from the collection
            available_tools.extend(collection.tools)
            console.print(f"[green]Successfully loaded tool collection with {len(collection.tools)} tools[/green]")
        except ToolLoadError:
            raise
        except Exception as e:
            raise ToolLoadError(
                f"Error loading tool collection ({tool_collection}): {str(e)}",
                "Check that the collection exists and you have proper permissions"
            )
    
    additional_imports = []
    if imports:
        additional_imports.extend(imports.split())
    
    try:
        return CodeAgent(
            tools=available_tools,
            model=model, 
            additional_authorized_imports=additional_imports
        )
    except Exception as e:
        raise AgentRuntimeError(
            f"Failed to initialize agent: {e}",
            "Check model configuration and tool compatibility"
        ) 