"""
Loader for tools from Hugging Face Hub.
"""
import os

from rich.console import Console
from smolagents import Tool, load_tool

from ..errors import ToolLoadError, AuthenticationError
from .base import ToolLoader

console = Console()


class HubToolLoader(ToolLoader):
    """Loader for tools from Hugging Face Hub"""
    def load(self, spec: str, **kwargs) -> Tool:
        """
        Load a tool from Hugging Face Hub.
        
        Args:
            spec: Hugging Face Hub repository ID
            
        Returns:
            The loaded tool
            
        Raises:
            ToolLoadError: If the tool cannot be loaded
        """
        try:
            repo_id = spec
            console.print(f"[bold blue]Loading tool from Hugging Face Hub: {repo_id}[/bold blue]")
            
            token = os.environ.get("HF_TOKEN")
            # Check if token is required but not provided
            if not token:
                raise AuthenticationError(
                    "No Hugging Face token provided for loading Hub tool",
                    "Set the HF_TOKEN environment variable or provide it directly"
                )
            
            hub_tool = load_tool(
                repo_id,
                trust_remote_code=True,
                token=token
            )
            return hub_tool
        except Exception as e:
            raise ToolLoadError(
                f"Error loading tool from Hub ({repo_id}): {str(e)}",
                "Check that the tool exists and you have proper permissions"
            ) 