import sys
from .errors import (
    XerusError, ModelInitializationError, AuthenticationError,
    ToolLoadError, ToolExecutionError, ModelNotFoundError,
    ModelConfigurationError, AgentRuntimeError, NetworkError,
    APILimitError, EnvironmentError, InputError
)
from .ui.display import console, print_error_panel, print_auth_error

def handle_command_errors(func):
    """Decorator to handle errors in CLI commands."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
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
    return wrapper 