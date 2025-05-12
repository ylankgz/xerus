"""
Tool management functionality for Xerus agents.
"""
import os
from pathlib import Path
from typing import Dict, List, Optional, Union, Any

from rich.console import Console
from smolagents import (
    Tool, WebSearchTool, PythonInterpreterTool, 
    FinalAnswerTool, UserInputTool, DuckDuckGoSearchTool, 
    VisitWebpageTool
)

from ..errors import ToolLoadError
from .built_in import BuiltInToolLoader
from .local import LocalFileToolLoader
from .hub import HubToolLoader
from .space import SpaceToolLoader
from .collection import CollectionToolLoader

console = Console()


class ToolManager:
    """
    Manager for loading, discovering, and validating tools for Xerus agents.
    
    This class centralizes all tool management functionality, including:
    - Loading tools from local files, Hugging Face Hub, and Spaces
    - Discovering tools in specified directories
    - Validating tool compatibility and dependencies
    - Managing built-in tools
    """
    
    def __init__(self):
        """Initialize the ToolManager with an empty registry."""
        self.tools: Dict[str, Tool] = {}
        self._register_built_in_tools()
        self._init_loaders()
    
    def _register_built_in_tools(self):
        """Register built-in tools that are always available."""
        # Register the web search tool with a consistent key
        self.tools["web_search"] = WebSearchTool()
        # Register additional default tools
        self.tools["python_interpreter"] = PythonInterpreterTool()
        self.tools["final_answer"] = FinalAnswerTool()
        self.tools["user_input"] = UserInputTool()
        self.tools["duckduckgo_search"] = DuckDuckGoSearchTool()
        self.tools["visit_webpage"] = VisitWebpageTool()
    
    def _init_loaders(self):
        """Initialize tool loaders for different tool types"""
        self.loaders = {
            "built_in": BuiltInToolLoader(self.tools),
            "local": LocalFileToolLoader(),
            "hub": HubToolLoader(),
            "space": SpaceToolLoader(),
            "collection": CollectionToolLoader()
        }
    
    def get_tool(self, tool_name: str) -> Optional[Tool]:
        """
        Get a specific tool by name.
        
        Args:
            tool_name: Name of the tool to retrieve
            
        Returns:
            The requested tool or None if not found
        """
        return self.tools.get(tool_name)
    
    def get_all_tools(self) -> List[Tool]:
        """
        Get all registered tools.
        
        Returns:
            List of all registered tools
        """
        return list(self.tools.values())
    
    def get_tools_by_names(self, tool_names: List[str]) -> List[Tool]:
        """
        Get specific tools by their names.
        
        Args:
            tool_names: List of tool names to retrieve
            
        Returns:
            List of requested tools (only those that exist)
        """
        return [self.tools[name] for name in tool_names if name in self.tools]
    
    def register_tool(self, tool: Tool) -> None:
        """
        Register a single tool with the manager.
        
        Args:
            tool: The Tool instance to register
        """
        self.tools[tool.name] = tool
        console.print(f"[green]Registered tool: {tool.name}[/green]")
    
    def load_from_local_file(self, file_path: str) -> List[Tool]:
        """
        Load tools from a local Python file.
        
        Args:
            file_path: Path to the Python file containing tool definitions
            
        Returns:
            List of loaded tools
            
        Raises:
            ToolLoadError: If the file cannot be loaded or contains no tools
        """
        tools = self.loaders["local"].load(file_path)
        for tool in tools:
            self.register_tool(tool)
        return tools
    
    def load_from_hub(self, repo_id: str) -> Tool:
        """
        Load a tool from Hugging Face Hub.
        Loading a tool means that you'll download the tool and execute it locally. ALWAYS inspect the tool you're downloading before loading it within your runtime, as you would do when installing a package using pip/npm/apt.
        
        Args:
            repo_id: Hugging Face Hub repository ID
            
        Returns:
            The loaded tool
            
        Raises:
            ToolLoadError: If the tool cannot be loaded
        """
        tool = self.loaders["hub"].load(repo_id)
        self.register_tool(tool)
        return tool
    
    def load_from_space(self, space_id: str, name: Optional[str] = None, 
                       description: Optional[str] = None) -> Tool:
        """
        Load a tool from Hugging Face Space.
        
        Args:
            space_id: Hugging Face Space ID
            name: Optional name for the tool (defaults to "space_tool")
            description: Optional description for the tool
            
        Returns:
            The loaded tool
            
        Raises:
            ToolLoadError: If the tool cannot be loaded
        """
        tool = self.loaders["space"].load(space_id, name=name, description=description)
        self.register_tool(tool)
        return tool
    
    def load_from_collection(self, collection_slug: str) -> List[Tool]:
        """
        Load tools from a Hugging Face Hub tool collection.
        
        Args:
            collection_slug: Hugging Face Hub repository ID for the tool collection
            trust_remote_code (defaults to False) — Whether to trust the remote code.
            
        Returns:
            List of loaded tools
            
        Raises:
            ToolLoadError: If the collection cannot be loaded or contains no tools
        """
        tools = self.loaders["collection"].load(collection_slug)
        for tool in tools:
            self.register_tool(tool)
        return tools
    
    def discover_tools(self, directory: str) -> List[Tool]:
        """
        Discover and load tools from Python files in the specified directory.
        
        Args:
            directory: Directory path to search for tool definitions
            
        Returns:
            List of discovered tools
        """
        discovered_tools = []
        directory_path = Path(directory)
        
        if not directory_path.exists() or not directory_path.is_dir():
            console.print(f"[yellow]Warning: Directory {directory} does not exist or is not a directory[/yellow]")
            return []
        
        # Iterate through all Python files in the directory
        for file_path in directory_path.glob("*.py"):
            try:
                tools = self.load_from_local_file(str(file_path))
                discovered_tools.extend(tools)
            except ToolLoadError as e:
                console.print(f"[yellow]Warning: Could not load tools from {file_path}: {e}[/yellow]")
        
        return discovered_tools
    
    def parse_tool_spec(self, tool_spec: str) -> Dict[str, Any]:
        """
        Parse a tool specification string into components.
        
        The tool spec can be in formats:
        - ["web_search", "python_interpreter", "final_answer", "user_input", "duckduckgo_search", "google_search", "visit_webpage"] - For built-in tools
        - "path/to/file.py" - For local files
        - "hub:repo_id" - For Hugging Face Hub tools
        - "space:space_id:name:description" - For Hugging Face Spaces
        - "collection:collection_slug" - For tool collections
        
        Args:
            tool_spec: Tool specification string
            
        Returns:
            Dictionary with parsed components
        """
        if ":" not in tool_spec:
            # Could be a built-in tool or a local file
            if tool_spec in self.tools:
                return {"type": "built_in", "name": tool_spec}
            elif os.path.exists(tool_spec) and tool_spec.endswith(".py"):
                return {"type": "local", "path": tool_spec}
            else:
                return {"type": "unknown", "spec": tool_spec}
        
        # Handle prefixed specifications
        parts = tool_spec.split(":", 2)
        prefix = parts[0].lower()
        
        if prefix == "hub" and len(parts) >= 2:
            return {"type": "hub", "repo_id": parts[1]}
        elif prefix == "space" and len(parts) >= 2:
            result = {"type": "space", "space_id": parts[1]}
            if len(parts) >= 3:
                # Further split the third part if it contains name:description
                name_desc = parts[2].split(":", 1)
                result["name"] = name_desc[0]
                if len(name_desc) > 1:
                    result["description"] = name_desc[1]
            return result
        elif prefix == "collection" and len(parts) >= 2:
            return {"type": "collection", "slug": parts[1]}
        else:
            return {"type": "unknown", "spec": tool_spec}
    
    def load_tool_from_spec(self, tool_spec: str) -> Union[Tool, List[Tool]]:
        """
        Load a tool or tools from a specification string.
        
        Args:
            tool_spec: Tool specification string
            
        Returns:
            Loaded tool(s)
            
        Raises:
            ToolLoadError: If the tool cannot be loaded
        """
        parsed = self.parse_tool_spec(tool_spec)
        
        if parsed["type"] == "built_in":
            return self.loaders["built_in"].load(parsed["name"])
        elif parsed["type"] == "local":
            return self.load_from_local_file(parsed["path"])
        elif parsed["type"] == "hub":
            return self.load_from_hub(parsed["repo_id"])
        elif parsed["type"] == "space":
            return self.load_from_space(
                parsed["space_id"],
                parsed.get("name"),
                parsed.get("description")
            )
        elif parsed["type"] == "collection":
            return self.load_from_collection(parsed["slug"])
        else:
            raise ToolLoadError(
                f"Unknown tool specification format: {tool_spec}",
                "Use one of the supported formats: built-in name, local file path, hub:repo_id, space:space_id[:name:desc], collection:slug"
            ) 