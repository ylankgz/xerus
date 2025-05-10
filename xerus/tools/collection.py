"""
Loader for tool collections from Hugging Face Hub.
"""
import os
from typing import List

from rich.console import Console
from smolagents import Tool, ToolCollection

from ..errors import ToolLoadError, AuthenticationError
from .base import ToolLoader

console = Console()


class CollectionToolLoader(ToolLoader):
    """Loader for tool collections from Hugging Face Hub"""
    def load(self, spec: str, **kwargs) -> List[Tool]:
        """
        Load tools from a Hugging Face Hub tool collection.
        
        Args:
            spec: Hugging Face Hub repository ID for the tool collection
            
        Returns:
            List of loaded tools
            
        Raises:
            ToolLoadError: If the collection cannot be loaded or contains no tools
        """
        try:
            collection_slug = spec
            console.print(f"[bold blue]Loading tool collection from Hub: {collection_slug}[/bold blue]")
            
            token = os.environ.get("HF_TOKEN")
            # Check if token is required but not provided
            if not token:
                raise AuthenticationError(
                    "No Hugging Face token provided for loading tool collection",
                    "Set the HF_TOKEN environment variable or provide it directly"
                )
            collection = ToolCollection.from_hub(
                collection_slug=collection_slug,
                trust_remote_code=True,
                token=token
            )
            
            if not collection.tools:
                raise ToolLoadError(
                    f"No tools found in collection: {collection_slug}",
                    "Verify that the collection exists and contains valid tools"
                )
                
            # Return all tools from the collection
            loaded_tools = list(collection.tools)
            console.print(f"[green]Successfully loaded tool collection with {len(loaded_tools)} tools[/green]")
            return loaded_tools
            
        except ToolLoadError:
            raise
        except Exception as e:
            raise ToolLoadError(
                f"Error loading tool collection ({collection_slug}): {str(e)}",
                "Check that the collection exists and you have proper permissions"
            ) 