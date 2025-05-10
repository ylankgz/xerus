"""
Base classes for tool loaders.
"""
from typing import List, Union

from smolagents import Tool

from ..errors import ToolLoadError


class ToolLoader:
    """Base class for tool loading strategies"""
    def load(self, spec: str, **kwargs) -> Union[Tool, List[Tool]]:
        """
        Load a tool or tools based on a specification.
        
        Args:
            spec: The specification for the tool
            **kwargs: Additional arguments for loading
            
        Returns:
            Loaded tool(s)
            
        Raises:
            ToolLoadError: If the tool cannot be loaded
        """
        raise NotImplementedError("Subclasses must implement this method") 