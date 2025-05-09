"""
Error handling module for Xerus package.
"""
from typing import Optional


class XerusError(Exception):
    """Base exception class for Xerus errors"""
    def __init__(self, message: str, recovery_hint: Optional[str] = None):
        self.message = message
        self.recovery_hint = recovery_hint
        super().__init__(message)


class ModelError(XerusError):
    """Base class for model-related errors"""
    pass


class ModelInitializationError(ModelError):
    """Error during model initialization"""
    pass


class ModelNotFoundError(ModelError):
    """Specified model could not be found"""
    pass


class ModelConfigurationError(ModelError):
    """Model configuration is invalid"""
    pass


class AuthenticationError(XerusError):
    """Authentication-related errors"""
    pass


class ToolError(XerusError):
    """Base class for tool-related errors"""
    pass


class ToolLoadError(ToolError):
    """Error loading a tool"""
    pass


class ToolExecutionError(ToolError):
    """Error during tool execution"""
    pass


class AgentRuntimeError(XerusError):
    """Error during agent execution"""
    pass


class InputError(XerusError):
    """Invalid input parameters"""
    pass


class NetworkError(XerusError):
    """Network-related errors"""
    pass


class APILimitError(XerusError):
    """API rate or quota limit reached"""
    def __init__(self, message: str, service: str = ""):
        recovery_hint = f"Consider reducing request frequency or upgrading your {service} plan."
        super().__init__(message, recovery_hint)


class EnvironmentError(XerusError):
    """Error related to environment setup"""
    pass


def get_recovery_hint(error_type: str) -> str:
    """Return recovery hints based on error type"""
    hints = {
        "AuthenticationError": "Check that your API keys are set correctly in environment variables or provided directly.",
        "ModelInitializationError": "Verify model ID and ensure you have proper permissions to access it.",
        "ModelNotFoundError": "Check that the model ID is correct and that you have access to it.",
        "ModelConfigurationError": "Review your model configuration parameters.",
        "ToolLoadError": "Ensure the tool path or ID is correct and that you have access to it.",
        "ToolExecutionError": "Check that the tool is functioning correctly and that inputs are valid.",
        "NetworkError": "Check your internet connection and try again later.",
        "APILimitError": "Wait before making more requests or upgrade your API plan.",
        "EnvironmentError": "Verify your Python environment has all required dependencies installed.",
        "InputError": "Review your command parameters and ensure they're correctly formatted."
    }
    return hints.get(error_type, "Please check your inputs and try again.") 