"""
OpenAI model implementations for Xerus.
"""
import os
from ..errors import AuthenticationError
from smolagents import OpenAIServerModel

def initialize_model(model_id, api_key=None, api_base=None, organization=None, project=None, 
                    client_kwargs=None, custom_role_conversions=None, flatten_messages_as_text=False, **kwargs):
    """
    Initialize and return an OpenAI model instance.
    
    Args:
        model_id: ID or name of the model, (e.g. "gpt-3.5-turbo").
        api_key: API key for OpenAI service
        api_base: The base URL of the OpenAI-compatible API server
        organization: The organization to use for the API request
        project: The project to use for the API request
        client_kwargs: Additional keyword arguments to pass to the OpenAI client, (e.g. "max_retries").
        custom_role_conversions: Custom role conversion mapping to convert message roles in others. Useful for specific models that do not support specific message roles like "system".
        flatten_messages_as_text: Whether to flatten messages as text
        **kwargs: Additional arguments to pass to the OpenAI API
        
    Returns:
        Initialized OpenAI model instance
        
    Raises:
        AuthenticationError: If authentication fails
        ModelInitializationError: If model initialization fails
    """
    api_key_val = api_key or os.environ.get("OPENAI_API_KEY")
    
    if not api_key_val:
        raise AuthenticationError(
            "No API key provided for OpenAI",
            f"Set the OPENAI_API_KEY environment variable or provide it via --api-key"
        )
    
    return OpenAIServerModel(
        model_id=model_id, 
        api_key=api_key_val,
        api_base=api_base,
        organization=organization,
        project=project,
        client_kwargs=client_kwargs,
        custom_role_conversions=custom_role_conversions,
        flatten_messages_as_text=flatten_messages_as_text,
        **kwargs
    ) 