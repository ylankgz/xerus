"""
Loader for tools from Hugging Face Spaces.
"""
import os
from typing import Optional

from rich.console import Console
from smolagents import Tool

from ..errors import ToolLoadError, AuthenticationError
from .base import ToolLoader

console = Console()


class SpaceToolLoader(ToolLoader):
    """Loader for tools from Hugging Face Spaces"""
    def load(self, spec: str, **kwargs) -> Tool:
        """
        Load a tool from Hugging Face Space.
        
        Args:
            spec: Hugging Face Space ID
            **kwargs: May include 'name' and 'description' for the tool
            
        Returns:
            The loaded tool
            
        Raises:
            ToolLoadError: If the tool cannot be loaded
        """
        try:
            space_id = spec
            name = kwargs.get("name") or "space_tool"
            description = kwargs.get("description") or f"Tool from Space {space_id}"
            
            console.print(f"[bold blue]Loading tool from Hugging Face Space: {space_id}[/bold blue]")
            
            token = os.environ.get("HF_TOKEN")
            # Check if token is required but not provided
            if not token:
                raise AuthenticationError(
                    "No Hugging Face token provided for loading Space tool",
                    "Set the HF_TOKEN environment variable or provide it directly"
                )
                
            
            space_tool = Tool.from_space(
                space_id,
                name=name,
                description=description,
                token=token,
                trust_remote_code=True
            )
            return space_tool
        except Exception as e:
            raise ToolLoadError(
                f"Error loading tool from Space ({space_id}): {str(e)}",
                "Check that the Space exists and is properly configured as a tool"
            ) 