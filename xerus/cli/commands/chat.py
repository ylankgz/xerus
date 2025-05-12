"""
Implementation of the 'chat' command for Xerus CLI.
"""
import sys
import json
import typer
from typing import Optional

from ...agent import create_agent, EnhancedAgent
from ...display import console, print_error_panel, print_auth_error
from ...errors import (
    XerusError, ModelInitializationError, AuthenticationError,
    ToolLoadError, ToolExecutionError, ModelNotFoundError,
    ModelConfigurationError, AgentRuntimeError, NetworkError,
    APILimitError, EnvironmentError, InputError
)
from ..sessions import (
    load_conversation_history,
    save_conversation_history,
    create_session_file,
    save_session
)
from ..progress import create_initialization_progress

def chat_command(
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
    no_history: bool = False,
    session_name: Optional[str] = None
):
    """Start an interactive chat session with the agent."""
    try:
        # Create progress for agent initialization
        progress = create_initialization_progress()
        
        agent_task = None
        
        with progress:
            # Add a task for agent initialization
            agent_task = progress.add_task("[bold green]Initializing agent...", total=100)
                        
            # Setup tools
            tool_list = tools.split(",") if tools else []
            tool_directories = tool_dirs.split(",") if tool_dirs else None
            
            # Parse JSON strings for client_kwargs and custom_role_conversions if provided
            role_conversions_dict = json.loads(custom_role_conversions) if custom_role_conversions else None
            
            # Create the agent with progress reporting
            base_agent = create_agent(
                model_id, api_key, tool_list, imports, 
                tool_local, tool_hub, tool_space, tool_collection,
                tool_directories, api_base=api_base,
                custom_role_conversions=role_conversions_dict,
                flatten_messages_as_text=flatten_messages_as_text,
                tool_name_key=tool_name_key,
                tool_arguments_key=tool_arguments_key,
                **(extra_params or {})
            )
            
            # Create enhanced agent
            agent = EnhancedAgent(base_agent)
            
            # Mark initialization as complete
            progress.update(agent_task, completed=100)
        
        # Load conversation history
        history = [] if no_history else load_conversation_history()
        if history and not no_history:
            console.print(f"[bold green]Loaded conversation history with {len(history)} messages[/bold green]")
        
        # Create a session file if a name is provided
        session_file = create_session_file(session_name) if session_name else None
        
        # Initialize session history
        session_history = []
            
        console.print("\n[bold blue]Interactive Chat Mode[/bold blue]")
        console.print("[green]Type 'exit', 'quit', or use Ctrl+C to end the session[/green]")
        console.print("[green]Type 'history' to view conversation history[/green]")
        console.print("[green]Type 'clear' to clear the conversation history[/green]")
        console.print("[green]Type 'save' to save the current session[/green]\n")
        
        # Main chat loop
        while True:
            try:
                # Get user input
                user_input = typer.prompt("You")
                
                # Check for exit commands
                if user_input.lower() in ["exit", "quit"]:
                    console.print("[bold blue]Exiting chat session[/bold blue]")
                    # Save session on exit if a name was provided
                    if session_name and session_file and session_history:
                        save_session(session_file, session_history, {
                            "model_id": model_id,
                            "output_format": output_format
                        })
                        console.print(f"[green]Session saved to {session_file}[/green]")
                    break
                
                # Check for history command
                if user_input.lower() == "history":
                    if not history:
                        console.print("[yellow]No conversation history yet.[/yellow]")
                    else:
                        for idx, entry in enumerate(history):
                            role = "[bold cyan]You[/bold cyan]" if entry["role"] == "user" else "[bold green]Agent[/bold green]"
                            console.print(f"{idx+1}. {role}: {entry['content'][:100]}{'...' if len(entry['content']) > 100 else ''}")
                    continue
                
                # Check for clear command
                if user_input.lower() == "clear":
                    history = []
                    agent.clear_history()
                    session_history = []
                    console.print("[yellow]Conversation history cleared.[/yellow]")
                    continue
                
                # Check for save command
                if user_input.lower() == "save":
                    if not session_history:
                        console.print("[yellow]No conversation to save yet.[/yellow]")
                        continue
                    
                    save_file = session_file or create_session_file(session_name)
                    save_session(save_file, session_history, {
                        "model_id": model_id,
                        "output_format": output_format
                    })
                    console.print(f"[green]Session saved to {save_file}[/green]")
                    continue
                
                # Process normal input
                history.append({"role": "user", "content": user_input})
                session_history.append({"role": "user", "content": user_input})
                
                # Create a context string from history
                include_history = len(history) > 1
                
                # Run the agent with context and history
                response = agent.run(
                    user_input, 
                    include_history=include_history,
                )
                
                # Add to histories
                history.append({"role": "assistant", "content": response})
                session_history.append({"role": "assistant", "content": response})
                
                # Save history if not disabled
                if not no_history:
                    save_conversation_history(history)
                    
            except KeyboardInterrupt:
                console.print("\n[bold blue]Chat session interrupted[/bold blue]")
                break
            except Exception as e:
                console.print(f"[bold red]Error during chat: {str(e)}[/bold red]")
                console.print("[green]You can continue chatting or type 'exit' to quit[/green]")
    
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