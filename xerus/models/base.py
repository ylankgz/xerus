"""
Base module for Xerus models.
"""
import os
import importlib

from ..errors import (
    ModelInitializationError, 
    AuthenticationError, 
    ModelNotFoundError,
    ModelConfigurationError,
    NetworkError
)

def get_model(model_type, model_id, **kwargs):
    """
    Create a model instance based on specified type.
    
    Args:
        model_type: Type of model to use ('inference', 'openai', 'litellm', 'transformers', 'mlx-lm')
        model_id: ID or name of the model
        **kwargs: Additional arguments to pass to the model initializer
    
    Returns:
        The initialized model instance
        
    Raises:
        ModelInitializationError: If model initialization fails
        ModelNotFoundError: If the specified model can't be found
        AuthenticationError: If authentication fails
        NetworkError: If there's a connection issue
    """
    # Map model_type to the corresponding module and model class
    model_map = {
        "inference": ("inference", "Inference"),
        "openai": ("openai", "OpenAI"),
        "litellm": ("litellm", "LiteLLM"),
        "transformers": ("transformers", "Transformer"),
        "mlx-lm": ("mlx", "MLX")
    }
    
    if model_type not in model_map:
        raise ModelConfigurationError(
            f"Unknown model type: {model_type}",
            f"Available model types: {', '.join(model_map.keys())}"
        )
    
    try:
        # Get module and class names from the mapping
        module_name, class_name = model_map[model_type]
        
        # Import the appropriate model module
        try:
            model_module = importlib.import_module(f"xerus.models.{module_name}")
            initialize_model = getattr(model_module, "initialize_model")
        except ImportError as e:
            raise ModelInitializationError(
                f"Failed to import model module: {e}",
                "Ensure all required packages are properly installed"
            )
        except AttributeError:
            raise ModelNotFoundError(
                f"initialize_model function not found in module '{module_name}'",
                "Check for package updates or choose a different model type"
            )
        
        # Initialize the model by delegating to module-specific initialize_model function
        try:
            return initialize_model(model_id=model_id, **kwargs)
        except Exception as e:
            # Let module-specific errors propagate
            raise
            
    except (ModelInitializationError, ModelNotFoundError, AuthenticationError) as e:
        # Re-raise these exceptions directly
        raise
    except ImportError as e:
        raise ModelInitializationError(
            f"Failed to import required module: {e}",
            "Check that all dependencies are installed correctly"
        )
    except ConnectionError as e:
        raise NetworkError(
            f"Connection error: {e}",
            "Check your internet connection and try again"
        )
    except Exception as e:
        # Check if it's an authentication error
        if any(x in str(e).lower() for x in ["401", "unauthorized", "authentication", "api key"]):
            raise AuthenticationError(
                "Authentication failed. Please check your API key or token.",
                "Verify that your credentials are correct and have not expired"
            )
        # Check if it could be a network issue
        elif any(x in str(e).lower() for x in ["timeout", "connection", "network", "unreachable"]):
            raise NetworkError(
                f"Network error occurred: {e}",
                "Check your internet connection and try again later"
            )
        else:
            raise ModelInitializationError(f"Failed to initialize model: {e}") 