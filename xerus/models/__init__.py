"""
Models package for Xerus.
Provides different model implementations.
"""
import warnings

# Try to load environment variables from .env file if python-dotenv is installed
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # Not raising an error since dotenv is optional
    warnings.warn(
        "python-dotenv package not installed. Environment variables from .env files will not be loaded. "
        "Install with: pip install python-dotenv"
    )

from .base import get_model
from .inference import InferenceClientModel
from .openai import OpenAIServerModel
from .litellm import LiteLLMModel
from .transformers import TransformersModel
from .mlx import MLXModel

__all__ = [
    "get_model",
    "InferenceClientModel", 
    "OpenAIServerModel",
    "MLXModel",
    "LiteLLMModel",
    "TransformersModel"
] 