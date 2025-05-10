"""
Loader for tools defined in local Python files.
"""
import importlib
import importlib.util
from typing import List

from rich.console import Console
from smolagents import Tool

from ..errors import ToolLoadError
from .base import ToolLoader

console = Console()


class LocalFileToolLoader(ToolLoader):
    """Loader for tools defined in local Python files"""
    def load(self, spec: str, **kwargs) -> List[Tool]:
        """
        Load tools from a local Python file.
        
        Args:
            spec: Path to the Python file containing tool definitions
            
        Returns:
            List of loaded tools
            
        Raises:
            ToolLoadError: If the file cannot be loaded or contains no tools
        """
        try:
            console.print(f"[bold blue]Loading tool from local file: {spec}[/bold blue]")
            # Import the module dynamically
            file_path = spec
            spec_obj = importlib.util.spec_from_file_location("local_tool", file_path)
            if not spec_obj:
                raise ToolLoadError(
                    f"Could not load spec from file: {file_path}",
                    "Ensure the file exists and is a valid Python module"
                )
                
            local_tool_module = importlib.util.module_from_spec(spec_obj)
            spec_obj.loader.exec_module(local_tool_module)
            
            # Find Tool instances in the module
            loaded_tools = []
            for name in dir(local_tool_module):
                obj = getattr(local_tool_module, name)
                if isinstance(obj, Tool):
                    loaded_tools.append(obj)
            
            if not loaded_tools:
                raise ToolLoadError(
                    f"No Tool instances found in {file_path}",
                    "Ensure the file contains properly defined Tool instances"
                )
                
            return loaded_tools
            
        except ToolLoadError:
            raise
        except Exception as e:
            raise ToolLoadError(f"Error loading tool from local file: {str(e)}") 