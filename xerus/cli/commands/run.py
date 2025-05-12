"""
Implementation of the 'run' command for Xerus CLI.
"""
import sys
import json
from typing import Optional

from ...agent import create_agent, EnhancedAgent
from ...display import console, print_error_panel, print_auth_error
from ...errors import (
    XerusError, ModelInitializationError, AuthenticationError,
    ToolLoadError, ToolExecutionError, ModelNotFoundError,
    ModelConfigurationError, AgentRuntimeError, NetworkError,
    APILimitError, EnvironmentError, InputError
)

from ..sessions import create_session_file, save_session
from ..progress import create_initialization_progress, create_task_progress_callback

def run_command(
    prompt: Optional[str] = None,
    model_id: Optional[str] = None,
    api_key: Optional[str] = None,
    api_base: Optional[str] = None,
    custom_role_conversions: Optional[str] = None,
    flatten_messages_as_text: Optional[bool] = None,
    tool_name_key: Optional[str] = None,
    tool_arguments_key: Optional[str] = None,
    extra_params: Optional[dict] = None,
    tools: Optional[str] = None,
    imports: Optional[str] = None,
    tool_local: Optional[str] = None,
    tool_hub: Optional[str] = None,
    tool_space: Optional[str] = None,
    tool_collection: Optional[str] = None,
    tool_dirs: Optional[str] = None,
    output_format: str = "rich",
    save_session: bool = False
):
    """Run the agent with a prompt."""
    try:
        # Check if prompt is None
        if prompt is None:
            raise InputError("No prompt provided. Please provide a text instruction for the agent to process.")
            
        # Create a progress instance for initialization
        progress = create_initialization_progress()
        
        agent_task = None
        
        with progress:
            # Add a task for agent initialization
            agent_task = progress.add_task("[bold green]Initializing agent...", total=100)
            
            # Progress callback function
            progress_callback = create_task_progress_callback(progress, agent_task)
            
            # Setup tools
            tool_list = tools.split(",") if tools else []
            tool_directories = tool_dirs.split(",") if tool_dirs else None
            
            # Parse JSON strings for client_kwargs and custom_role_conversions if provided
            role_conversions_dict = json.loads(custom_role_conversions) if custom_role_conversions else None
            
            # Create the agent with progress reporting
            base_agent = create_agent(
                model_id, api_key, tool_list, imports, 
                tool_local, tool_hub, tool_space, tool_collection,
                tool_directories, progress_callback=progress_callback,
                api_base=api_base,
                custom_role_conversions=role_conversions_dict,
                flatten_messages_as_text=flatten_messages_as_text,
                tool_name_key=tool_name_key,
                tool_arguments_key=tool_arguments_key,
                **(extra_params or {})
            )
            
            # Create the enhanced agent
            agent = EnhancedAgent(base_agent)
            
            # Mark initialization as complete
            progress.update(agent_task, completed=100)
                
        response = agent.run(prompt)
        
        # Save session if requested
        if save_session:
            session_file = create_session_file()
            save_session(session_file, [
                {"role": "user", "content": prompt},
                {"role": "assistant", "content": response}
            ], {
                "model_id": model_id,
                "output_format": output_format
            })
            console.print(f"[green]Session saved to {session_file}[/green]")
    
    except AuthenticationError as e:
        print_auth_error(str(e), e.recovery_hint)
        sys.exit(1)
    except ModelNotFoundError as e:
        print_error_panel("Model Not Found", str(e), "Model Error", e.recovery_hint)
        sys.exit(1)
    except ModelInitializationError as e:
        print_error_panel("Model Error", str(e), "Model Initialization Failed", e.recovery_hint)
        sys.exit(1)
    except ModelConfigurationError as e:
        print_error_panel("Configuration Error", str(e), "Model Configuration Error", e.recovery_hint)
        sys.exit(1)
    except ToolLoadError as e:
        print_error_panel("Tool Error", str(e), "Tool Loading Failed", e.recovery_hint)
        sys.exit(1)
    except ToolExecutionError as e:
        print_error_panel("Tool Error", str(e), "Tool Execution Failed", e.recovery_hint)
        sys.exit(1)
    except NetworkError as e:
        print_error_panel("Network Error", str(e), "Connection Failed", e.recovery_hint)
        sys.exit(1)
    except APILimitError as e:
        print_error_panel("API Limit Error", str(e), "API Limit Reached", e.recovery_hint)
        sys.exit(1)
    except AgentRuntimeError as e:
        print_error_panel("Agent Error", str(e), "Execution Failed", e.recovery_hint)
        sys.exit(1)
    except EnvironmentError as e:
        print_error_panel("Environment Error", str(e), "Environment Setup Failed", e.recovery_hint)
        sys.exit(1)
    except InputError as e:
        print_error_panel("Input Error", str(e), "Invalid Input", e.recovery_hint)
        sys.exit(1)
    except XerusError as e:
        print_error_panel("Xerus Error", str(e), "Error", e.recovery_hint)
        sys.exit(1)
    except Exception as e:
        print_error_panel("Unexpected Error", str(e), "Unhandled Error", 
                         "Please report this issue to the Xerus developers")
        sys.exit(1) 