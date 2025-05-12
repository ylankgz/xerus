"""
Models package for Xerus.
Provides different model implementations.
"""

from .base import get_model
from .litellm import LiteLLMModel

__all__ = [
    "get_model",
    "LiteLLMModel",
] 