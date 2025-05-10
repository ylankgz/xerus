"""
MLX model implementation for Xerus.
"""
from smolagents import MLXModel


def initialize_model(
    model_id,
    tool_name_key=None,
    tool_arguments_key=None,
    trust_remote_code=False,
    **kwargs
):
    """
    Initialize and return a LiteLLM model instance.
    
    Args:
        model_id: ID or name of the model (e.g. "HuggingFaceTB/SmolLM-135M-Instruct").
        tool_name_key: The key, which can usually be found in the model's chat template, for retrieving a tool name.
        tool_arguments_key: The key, which can usually be found in the model's chat template, for retrieving tool arguments.
        trust_remote_code: Some models on the Hub require running remote code.
        **kwargs: Any additional keyword arguments that you want to use in model.generate(). (e.g. max_tokens)
        
    Returns:
        Initialized MLX model instance
        
    Raises:
        AuthenticationError: If authentication fails
        ModelInitializationError: If model initialization fails
    """
    
    return MLXModel(
        model_id=model_id, 
        tool_name_key=tool_name_key,
        tool_arguments_key=tool_arguments_key,
        trust_remote_code=trust_remote_code,
        **kwargs
    ) 