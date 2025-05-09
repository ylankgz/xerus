"""
Xerus - CLI Agent powered by Huggingface Smolagents

A command-line interface for running AI agents that can perform tasks,
search the web, and execute code, all powered by large language models.
"""

__version__ = "0.1.0"

# Import key functions to make them available at package level
from .cli import create_agent, cli, run 