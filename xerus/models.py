"""
Models module for Xerus package.
"""
import os
import importlib

from .errors import (
    ModelInitializationError, 
    AuthenticationError, 
    ModelNotFoundError,
    ModelConfigurationError,
    NetworkError
)


def get_model(model_type, model_id, api_key=None):
    """
    Create a model instance based on specified type.
    
    Args:
        model_type: Type of model to use ('inference', 'openai', 'litellm', 'transformers')
        model_id: ID or name of the model
        api_key: API key for the model service
    
    Returns:
        The initialized model instance
        
    Raises:
        ModelInitializationError: If model initialization fails
        ModelNotFoundError: If the specified model can't be found
        AuthenticationError: If authentication fails
        NetworkError: If there's a connection issue
    """
    # Map model_type to the corresponding class name
    model_class_map = {
        "inference": "InferenceClientModel",
        "openai": "OpenAIServerModel",
        "azure-openai": "AzureOpenAIServerModel",
        "amazon-bedrock": "AmazonBedrockServerModel",
        "mlx-lm": "MLXModel",
        "litellm": "LiteLLMModel",
        "transformers": "TransformersModel"
    }
    
    if model_type not in model_class_map:
        raise ModelConfigurationError(
            f"Unknown model type: {model_type}",
            f"Available model types: {', '.join(model_class_map.keys())}"
        )
    
    try:
        # Dynamically import the appropriate model class
        model_class_name = model_class_map[model_type]
        try:
            ModelClass = getattr(importlib.import_module("smolagents.models"), model_class_name)
        except ImportError as e:
            raise ModelInitializationError(
                f"Failed to import model class: {e}",
                "Ensure smolagents package is properly installed with 'pip install smolagents'"
            )
        except AttributeError:
            raise ModelNotFoundError(
                f"Model class '{model_class_name}' not found in smolagents package",
                "Check for package updates or choose a different model type"
            )
        
        # Initialize and return the model based on its type
        if model_type == "inference":
            try:
                return ModelClass(model_id=model_id)
            except Exception as e:
                if "404" in str(e):
                    raise ModelNotFoundError(f"Model '{model_id}' not found on Hugging Face Hub")
                raise
        elif model_type in ["openai", "azure-openai"]:
            api_key_env = "OPENAI_API_KEY"
            api_key_val = api_key or os.environ.get(api_key_env)
            if not api_key_val:
                raise AuthenticationError(
                    f"No API key provided for {model_type}",
                    f"Set the {api_key_env} environment variable or provide it via --api-key"
                )
            return ModelClass(model_id=model_id, api_key=api_key_val)
        elif model_type == "amazon-bedrock":
            aws_access_key = os.environ.get("AWS_ACCESS_KEY_ID")
            aws_secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
            aws_region = os.environ.get("AWS_REGION", "us-east-1")
            
            if not aws_access_key or not aws_secret_key:
                raise AuthenticationError(
                    "Missing AWS credentials",
                    "Set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables"
                )
            
            return ModelClass(
                model_id=model_id,
                aws_access_key=aws_access_key,
                aws_secret_key=aws_secret_key,
                aws_region=aws_region
            )
        elif model_type == "litellm":
            api_key_env = "LITELLM_API_KEY"
            api_key_val = api_key or os.environ.get(api_key_env)
            if not api_key_val:
                raise AuthenticationError(
                    f"No API key provided for {model_type}",
                    f"Set the {api_key_env} environment variable or provide it via --api-key"
                )
            return ModelClass(model_id=model_id, api_key=api_key_val)
        elif model_type == "transformers":
            return ModelClass(
                model_id=model_id,
                max_new_tokens=4096,
                device_map="auto"
            )
        elif model_type == "mlx-lm":
            return ModelClass(
                model_id=model_id,
                max_tokens=4096
            )
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