import os
import importlib.util
from typing import List, Optional

from smolagents import (
    Tool, WebSearchTool, PythonInterpreterTool, 
    FinalAnswerTool, UserInputTool, DuckDuckGoSearchTool, 
    VisitWebpageTool, ToolCollection, load_tool
)

from .agent import create_tool_agent
from .ui.display import console

def setup_built_in_tools(model_id: str, api_key: str, api_base: str):
    """Setup and return built-in tools as agent list."""
    tools = [
        {
            "tool": WebSearchTool(), 
            "name": "web_search_agent",
            "description": "Searches the web for information"
        },
        {
            "tool": PythonInterpreterTool(),
            "name": "python_interpreter_agent",
            "description": "Executes Python code"
        },
        {
            "tool": FinalAnswerTool(),
            "name": "final_answer_agent",
            "description": "Provides the final answer to the user"
        },
        {
            "tool": UserInputTool(),
            "name": "user_input_agent",
            "description": "Accepts user input"
        },
        {
            "tool": DuckDuckGoSearchTool(),
            "name": "duckduckgo_search_agent",
            "description": "Searches the web for information using DuckDuckGo"
        },
        {
            "tool": VisitWebpageTool(),
            "name": "visit_webpage_agent",
            "description": "Visits a webpage"
        }
    ]

    built_in_tools_agents_list = []

    for tool in tools:
        built_in_tools_agents_list.append(
            create_tool_agent(
                model_id,
                api_key,
                api_base,
                [tool["tool"]],
                name=tool["name"],
                description=tool["description"]
            )
        )

    return built_in_tools_agents_list


def setup_local_tools(local_tools_path: Optional[str], model_id: str, api_key: str, api_base: str):
    """Setup and return local tools as agent list."""
    local_tools_agents_list = []
    
    if not local_tools_path:
        return local_tools_agents_list
    
    tool_index = 0
    for tool_spec in local_tools_path.split(","):
        if os.path.exists(tool_spec) and tool_spec.endswith(".py"):
            spec_obj = importlib.util.spec_from_file_location("local_tool", tool_spec)
            if not spec_obj:
                continue
            local_tool_module = importlib.util.module_from_spec(spec_obj)
            spec_obj.loader.exec_module(local_tool_module)
            for name in dir(local_tool_module):
                obj = getattr(local_tool_module, name)
                if isinstance(obj, Tool):
                    local_tools_agents_list.append(create_tool_agent(
                        model_id,
                        api_key,
                        api_base,
                        [obj],
                        name=obj.name,
                        description=obj.description
                    ))
                    tool_index += 1
                    
    return local_tools_agents_list

def setup_huggingface_tools(
    model_id: str, 
    api_key: str, 
    api_base: str,
    hub_tools: Optional[str] = None,
    space_tools: Optional[str] = None,
    collection_tools: Optional[str] = None
):
    """Setup and return Hugging Face tools as agent list."""
    space_tools_agents_list = []
    collection_tools_agents_list = []
    hub_tools_agents_list = []

    token = os.environ.get("HF_TOKEN")
    if not token:
        console.print("[yellow]Warning: No Hugging Face token provided for loading Space, Hub or Collections tools[/yellow]")
        return [], [], []
        
    # Setup space tools
    if space_tools:
        for i, tool_spec in enumerate(space_tools.split(",")):
            parts = tool_spec.split(":")
            space_id = parts[0]
            name = parts[1]
            description = parts[2] if len(parts) > 2 else ""
            space_tools_agents_list.append(create_tool_agent(
                model_id,
                api_key,
                api_base,
                Tool.from_space(space_id, name=name, description=description, token=token),
                name=name,
                description=description
            ))
    
    # Setup collection tools
    if collection_tools:
        for i, tool_spec in enumerate(collection_tools.split(",")):
            tool_collection = ToolCollection.from_hub(tool_spec, token=token)
            collection_tools_agents_list.append(create_tool_agent(
                model_id,
                api_key,
                api_base,
                [*tool_collection.tools],
            ))

    # Setup hub tools
    if hub_tools:
        for i, tool_spec in enumerate(hub_tools.split(",")):
            hub_tool = load_tool(tool_spec, token=token, trust_remote_code=True)
            hub_tools_agents_list.append(create_tool_agent(
                model_id,
                api_key,
                api_base,
                [hub_tool],
                name=hub_tool.name,
                description=hub_tool.description
            ))
            
    return space_tools_agents_list, collection_tools_agents_list, hub_tools_agents_list 