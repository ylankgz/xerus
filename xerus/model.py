from typing import Optional, Dict, Callable
from smolagents import LiteLLMModel

from .errors import (
    AuthenticationError,
    ModelNotFoundError,
    InputError,
    ModelInitializationError,
    NetworkError
)

class ModelFactory:
    @staticmethod
    def create_client(
        model_id: Optional[str],
        api_key: Optional[str],
        api_base: Optional[str],
        **kwargs,
    ) -> LiteLLMModel:
        """
        Initialize and return a LiteLLM model instance.
        
        Args:
            model_id: ID or name of the model (e.g. "anthropic/claude-3-5-sonnet-latest").
            api_key: API key for LiteLLM service
            api_base: The base URL of the provider API to call the model.
            **kwargs: Additional keyword arguments to pass to the OpenAI API. (e.g. temperature, max_tokens, etc.)
            
        Returns:
            Initialized LiteLLM model instance
            
        Raises:
            ModelNotFoundError: If no model ID is provided
            AuthenticationError: If authentication fails
            ModelInitializationError: If model initialization fails
            NetworkError: If there's a connection issue
        """
        if model_id is None:
            raise ModelNotFoundError("No model ID provided. Please provide a valid model ID.")
        if api_key is None:
            raise AuthenticationError("No API key provided. Please provide a valid API key.")
        
        try:
            # Initialize the model by delegating to module-specific initialize_model function
            try:
                return LiteLLMModel(
                    model_id=model_id, 
                    api_key=api_key,
                    api_base=api_base,
                    **kwargs
                )
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
                
