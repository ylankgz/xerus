"""
Inference model implementation for Xerus.
"""
import os
from smolagents import InferenceClientModel
from ..errors import ModelInitializationError, ModelNotFoundError

def initialize_model(
    model_id="Qwen/Qwen2.5-Coder-32B-Instruct",
    provider="hf-inference",
    token=None,
    timeout=120,
    client_kwargs=None,
    custom_role_conversions=None,
    bill_to=None,
    **kwargs
):
    """
    Initialize and return an InferenceClientModel instance.
    
    Args:
        model_id (str, optional): ID or name of the model on HuggingFace Hub. Defaults to "Qwen/Qwen2.5-Coder-32B-Instruct".
        token (str, optional): Token for authentication. Defaults to HF_TOKEN environment variable.
        provider (str, optional): Name of the provider to use for inference. Defaults to "hf-inference".
        timeout (int, optional): Timeout for the API request, in seconds. Defaults to 120.
        client_kwargs (dict, optional): Additional keyword arguments for the Hugging Face InferenceClient. Defaults to None.
        custom_role_conversions (dict, optional): Custom role conversion mapping. Defaults to None.
        bill_to (str, optional): The billing account to use for the requests. Defaults to None.
        **kwargs: Additional keyword arguments to pass to the Hugging Face API.
        
    Returns:
        Initialized InferenceClientModel instance
        
    Raises:
        ModelNotFoundError: If the specified model can't be found
        ModelInitializationError: If model initialization fails
    """
    try:
        return InferenceClientModel(
            model_id=model_id,
            provider=provider,
            token=token,
            timeout=timeout,
            client_kwargs=client_kwargs,
            custom_role_conversions=custom_role_conversions,
            bill_to=bill_to,
            **kwargs
        )
    except Exception as e:
        if "404" in str(e):
            raise ModelNotFoundError(f"Model '{model_id}' not found on Hugging Face Hub")
        raise ModelInitializationError(f"Failed to initialize inference model: {e}") 