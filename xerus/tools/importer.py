import importlib.util
from typing import Optional, Type

from ..ui.display import console


class ToolImporter:
    """Handles dynamic importing of tool classes."""
    
    @staticmethod
    def import_tool_class(tool_class_path: str) -> Optional[Type]:
        """
        Dynamically import a tool class from its module path.
        
        Args:
            tool_class_path: Full module path to the tool class (e.g., 'module.submodule.ClassName')
            
        Returns:
            The imported tool class, or None if import failed
        """
        try:
            module_path, class_name = tool_class_path.rsplit('.', 1)
            module = importlib.import_module(module_path)
            tool_class = getattr(module, class_name)
            return tool_class
        except (ImportError, AttributeError, ValueError) as e:
            console.print(f"[red]Error importing tool class '{tool_class_path}': {e}[/red]")
            return None 