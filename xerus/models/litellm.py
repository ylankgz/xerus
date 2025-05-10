"""
LiteLLM model implementation for Xerus.
"""
import os
from smolagents import LiteLLMModel
from ..errors import AuthenticationError


def initialize_model(model_id, api_key=None, api_base=None, custom_role_conversions=None, 
                    flatten_messages_as_text=None, **kwargs):
    """
    Initialize and return a LiteLLM model instance.
    
    Args:
        model_id: ID or name of the model (e.g. "anthropic/claude-3-5-sonnet-latest").
        api_key: API key for LiteLLM service
        api_base: The base URL of the provider API to call the model.
        custom_role_conversions: Custom role conversion mapping to convert message roles in others. 
            Useful for specific models that do not support specific message roles like "system".
        flatten_messages_as_text: Whether to flatten messages as text. 
            Defaults to True for models that start with "ollama", "groq", "cerebras".
        **kwargs: Additional keyword arguments to pass to the OpenAI API. (e.g. temperature, max_tokens, etc.)
        
    Returns:
        Initialized LiteLLM model instance
        
    Raises:
        AuthenticationError: If authentication fails
        ModelInitializationError: If model initialization fails
    """
    api_key_val = api_key or os.environ.get("LITELLM_API_KEY")
    
    if not api_key_val:
        raise AuthenticationError(
            "No API key provided for LiteLLM",
            f"Set the LITELLM_API_KEY environment variable or provide it via --api-key"
        )
    
    return LiteLLMModel(
        model_id=model_id, 
        api_key=api_key_val,
        api_base=api_base,
        custom_role_conversions=custom_role_conversions,
        flatten_messages_as_text=flatten_messages_as_text,
        **kwargs
    ) 