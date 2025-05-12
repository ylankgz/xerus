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
from .litellm import initialize_model

def get_model(model_id, **kwargs):
    """
    Create a model instance based on specified type.
    
    Args:
        model_id: ID or name of the model
        **kwargs: Additional arguments to pass to the model initializer. Any extra parameters 
                 provided will be forwarded directly to the model-specific initialize_model 
                 function and ultimately to the underlying model API.
    
    Returns:
        The initialized model instance
        
    Raises:
        ModelInitializationError: If model initialization fails
        ModelNotFoundError: If the specified model can't be found
        AuthenticationError: If authentication fails
        NetworkError: If there's a connection issue
    """

    try:
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