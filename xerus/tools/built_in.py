"""
Loader for built-in tools.
"""
from typing import Dict

from rich.console import Console
from smolagents import Tool

from ..errors import ToolLoadError
from .base import ToolLoader

console = Console()


class BuiltInToolLoader(ToolLoader):
    """Loader for built-in tools"""
    def __init__(self, tool_registry: Dict[str, Tool]):
        """
        Initialize with a registry of available built-in tools.
        
        Args:
            tool_registry: Dictionary mapping tool names to Tool instances
        """
        self.tool_registry = tool_registry
        
    def load(self, spec: str, **kwargs) -> Tool:
        """
        Load a built-in tool by name.
        
        Args:
            spec: The name of the built-in tool
            
        Returns:
            The built-in tool
            
        Raises:
            ToolLoadError: If the built-in tool is not found
        """
        if spec not in self.tool_registry:
            raise ToolLoadError(
                f"Built-in tool not found: {spec}",
                "Available built-in tools: " + ", ".join(self.tool_registry.keys())
            )
        return self.tool_registry[spec] 