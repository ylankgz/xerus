"""
Transformers model implementation for Xerus.
"""
from ..errors import ModelInitializationError, ModelNotFoundError
from smolagents import TransformersModel

def initialize_model(model_id, device_map=None, torch_dtype=None, trust_remote_code=False, **kwargs):
    """
    Initialize and return a TransformersModel instance.
    
    Args:
        model_id (str): The Hugging Face model ID to be used for inference
        device_map (str, optional): The device_map to initialize your model with.
        torch_dtype (str, optional): The torch_dtype to initialize your model with
        trust_remote_code (bool, optional): Whether to trust remote code for models from the Hub
        **kwargs: Additional keyword arguments to pass to model.generate()
        
    Returns:
        Initialized TransformersModel instance
        
    Raises:
        ModelNotFoundError: If the specified model can't be found
        ModelInitializationError: If model initialization fails
    """
    try:
        return TransformersModel(
            model_id=model_id,
            device_map=device_map,
            torch_dtype=torch_dtype,
            trust_remote_code=trust_remote_code,
            **kwargs
        )
    except Exception as e:
        if "model not found" in str(e).lower() or "404" in str(e):
            raise ModelNotFoundError(f"Model '{model_id}' not found")
        raise ModelInitializationError(f"Failed to initialize Transformers model: {e}") 