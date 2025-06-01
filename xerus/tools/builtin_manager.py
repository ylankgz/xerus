from typing import List, Dict, Any
from smolagents import CodeAgent

from ..ui.display import console
from .factory import ToolAgentFactory
from .importer import ToolImporter


class BuiltInToolsManager:
    """Manages built-in tools loading and agent creation."""
    
    def __init__(self):
        self.tool_importer = ToolImporter()
        self.tool_factory = ToolAgentFactory()
    
    def load_tools_from_config(self, config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Load built-in tools from configuration.
        
        Args:
            config: Configuration dictionary
            
        Returns:
            List of tool configuration dictionaries
        """
        tools = []
        tool_configs = config.get('tools', {})
        
        for tool_name, tool_config in tool_configs.items():
            # Get tool class path from config
            tool_class_path = tool_config.get("tool_class")
            if not tool_class_path:
                console.print(f"[yellow]Warning: No tool_class specified for {tool_name}, skipping[/yellow]")
                continue
            
            # Dynamically import the tool class
            tool_class = self.tool_importer.import_tool_class(tool_class_path)
            if not tool_class:
                console.print(f"[yellow]Warning: Could not load tool class for {tool_name}, skipping[/yellow]")
                continue
            
            # Get tool parameters from config
            tool_params = tool_config.get("parameters", {})
            
            # Create tool instance with parameters using universal approach
            try:
                tool_instance = tool_class(**tool_params)
            except TypeError as e:
                # If tool doesn't accept the parameters, try without them
                console.print(f"[yellow]Warning: Tool {tool_name} doesn't accept some parameters: {e}[/yellow]")
                console.print(f"[yellow]Creating {tool_name} without parameters[/yellow]")
                try:
                    tool_instance = tool_class()
                except Exception as e2:
                    console.print(f"[red]Error creating tool {tool_name}: {e2}[/red]")
                    continue
            
            tools.append({
                "tool": tool_instance,
                "name": tool_config.get("name", tool_name),
                "description": tool_config.get("description", ""),
                "model_id": tool_config.get("model_id", ""),
                "api_key": tool_config.get("api_key", ""),
                "api_base": tool_config.get("api_base", ""),
                "code_agent": tool_config.get("code_agent", True)
            })
        
        return tools
    
    def create_tool_agents(self, tools: List[Dict[str, Any]]) -> List[CodeAgent]:
        """
        Create CodeAgent instances from tool configurations.
        
        Args:
            tools: List of tool configuration dictionaries
            
        Returns:
            List of created CodeAgent instances
        """
        built_in_tools_agents_list = []
        
        for tool in tools:
            try:
                agent = self.tool_factory.create_agent(
                    tool["model_id"],
                    tool["api_key"],
                    tool["api_base"],
                    [tool["tool"]],
                    name=tool["name"],
                    description=tool["description"],
                    code_agent=tool["code_agent"]
                )
                built_in_tools_agents_list.append(agent)
            except Exception as e:
                console.print(f"[red]Error creating agent for tool '{tool['name']}': {e}[/red]")
                continue
        
        return built_in_tools_agents_list 