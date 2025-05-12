"""
Agent module for Xerus package.
"""
from typing import Optional

from rich.console import Console
from smolagents import CodeAgent

from .models import get_model
from .tools.manager import ToolManager
from .errors import (
    ToolLoadError,
    AgentRuntimeError
)

console = Console()

def create_agent(
    model_id,
    api_key=None,
    tools=None,
    imports=None, 
    tool_local=None,
    tool_hub=None,
    tool_space=None,
    tool_collection=None,
    tool_dirs=None,
    api_base=None,
    custom_role_conversions=None,
    flatten_messages_as_text=False,
    tool_name_key=None,
    tool_arguments_key=None,
    **kwargs
):
    """
    Create a CodeAgent with specified model and tools.
    
    Args:
        model_id: ID or name of the model
        api_key: API key for the model service
        tools: List of tool names or specifications to enable
        imports: List of Python packages to authorize for import
        tool_local: Path to a local tool file
        tool_hub: Hugging Face Hub repo ID for a tool
        tool_space: Hugging Face Space ID to import as a tool
        tool_collection: Hugging Face Hub repo ID for a collection of tools
        tool_dirs: List of directories to discover tools from
        api_base: The base URL of the API server (for OpenAI and similar APIs)
        custom_role_conversions: Custom role conversion mapping (for OpenAI)
        flatten_messages_as_text: Whether to flatten messages as text (for OpenAI)
        tool_name_key: The key for retrieving a tool name (for transformers/MLX models)
        tool_arguments_key: The key for retrieving tool arguments (for transformers/MLX models)
        **kwargs: Additional model-specific arguments that will be passed directly to the underlying model API
    
    Returns:
        The initialized CodeAgent
        
    Raises:
        ModelInitializationError: If model initialization fails
        ToolLoadError: If a tool fails to load
        AgentRuntimeError: For other agent setup errors
    """
    
    model = get_model(
        model_id, 
        api_key=api_key,
        api_base=api_base,
        custom_role_conversions=custom_role_conversions,
        flatten_messages_as_text=flatten_messages_as_text,
        tool_name_key=tool_name_key,
        tool_arguments_key=tool_arguments_key,
        **kwargs
    )
    
    # Initialize the tool manager
    tool_manager = ToolManager()
    available_tools = []
    
    tool_count = sum(1 for x in [tools, tool_local, tool_hub, tool_space, tool_collection, tool_dirs] if x)
    tool_progress = 0.3
    tool_progress_increment = 0.4 / max(1, tool_count) if tool_count > 0 else 0
    
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
                console.print(f"[yellow]Warning: Failed to load tool '{tool_spec}': {e}[/yellow]\n")
        tool_progress += tool_progress_increment
    
    # Load tools from additional sources
    if tool_local:
        try:
            local_tools = tool_manager.load_from_local_file(tool_local)
            available_tools.extend(local_tools)
        except ToolLoadError as e:
            raise ToolLoadError(str(e))
        tool_progress += tool_progress_increment
    
    if tool_hub:
        try:
            hub_tool = tool_manager.load_from_hub(tool_hub)
            available_tools.append(hub_tool)
        except ToolLoadError as e:
            raise ToolLoadError(str(e))
        tool_progress += tool_progress_increment
    
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
        tool_progress += tool_progress_increment
    
    if tool_collection:
        try:
            collection_tools = tool_manager.load_from_collection(tool_collection)
            available_tools.extend(collection_tools)
        except ToolLoadError as e:
            raise ToolLoadError(str(e))
        tool_progress += tool_progress_increment
    
    # Discover tools from directories
    if tool_dirs:
        for directory in tool_dirs:
            try:
                discovered_tools = tool_manager.discover_tools(directory)
                available_tools.extend(discovered_tools)
                console.print(f"[green]Discovered {len(discovered_tools)} tools in {directory}[/green]\n")
            except Exception as e:
                console.print(f"[yellow]Warning: Error discovering tools in {directory}: {e}[/yellow]\n")
    
    # Get unique tools based on name
    unique_tools = {}
    for tool in available_tools:
        unique_tools[tool.name] = tool
    
    additional_imports = []
    if imports:
        additional_imports.extend(imports.split(","))
    
    try:
        agent = CodeAgent(
            tools=list(unique_tools.values()),
            model=model, 
            additional_authorized_imports=additional_imports
        )
        
        return agent
    except Exception as e:
        raise AgentRuntimeError(
            f"Failed to initialize agent: {e}",
            "Check model configuration and tool compatibility"
        ) 

class EnhancedAgent:
    """
    Enhanced agent with additional features beyond the base CodeAgent.
    
    This class wraps the CodeAgent and adds:
    - Conversation history management
    - Progress reporting
    - Better error handling and recovery
    - Tool execution monitoring
    """
    
    def __init__(self, code_agent: CodeAgent):
        """
        Initialize the enhanced agent with a CodeAgent instance.
        
        Args:
            code_agent: The CodeAgent instance to enhance
        """
        self.agent = code_agent
        self.history = []
    
    def run(
        self,
        prompt: str,
        context: Optional[str] = None,
        include_history: bool = False,
    ) -> str:
        """
        Run the agent with the given prompt.
        
        Args:
            prompt: The user's prompt text
            context: Optional additional context for the prompt
            include_history: Whether to include conversation history
            
        Returns:
            The agent's response
            
        Raises:
            ToolExecutionError: If a tool fails to execute
            AgentRuntimeError: For other runtime errors
        """
        # Build the complete prompt with context and history if needed
        complete_prompt = prompt
        
        if context:
            complete_prompt = f"{context}\n\n{prompt}"
            
        if include_history and self.history:
            history_text = "\n\n".join([
                f"User: {item['user']}\nAgent: {item['agent']}"
                for item in self.history[-5:]  # Include the last 5 exchanges
            ])
            complete_prompt = f"Previous conversation:\n{history_text}\n\nUser: {complete_prompt}"
        
        try:            
            # Execute the agent with the complete prompt
            response = self.agent.run(complete_prompt)
            
            # Update history
            self.history.append({
                "user": prompt,
                "agent": response
            })
            
            return response
            
        except Exception as e:
            raise AgentRuntimeError(
                f"Error running agent: {str(e)}",
                "Check your prompt and try again with more specific instructions"
            )
    
    def get_history(self):
        """Get the conversation history."""
        return self.history
    
    def clear_history(self):
        """Clear the conversation history."""
        self.history = [] 