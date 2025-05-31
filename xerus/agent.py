"""
Agent module for Xerus package.
"""
import os
from typing import Optional, List

from rich.console import Console
from smolagents import CodeAgent, Tool

from .model import ModelFactory
from .errors import (
    AgentRuntimeError
)

console = Console()
    
class EnhancedAgent:
    """
    Enhanced agent with additional features beyond the base CodeAgent.
    
    This class wraps the CodeAgent and adds:
    - Conversation history management
    - Progress reporting
    - Better error handling and recovery
    - Tool execution monitoring
    """
    
    def __init__(self, code_agent: CodeAgent):
        """
        Initialize the enhanced agent with a CodeAgent instance.
        
        Args:
            code_agent: The CodeAgent instance to enhance
        """
        self.agent = code_agent
        self.history = []
    
    def run(
        self,
        prompt: str,
        context: Optional[str] = None,
        include_history: bool = False,
    ) -> str:
        """
        Run the agent with the given prompt.
        
        Args:
            prompt: The user's prompt text
            context: Optional additional context for the prompt
            include_history: Whether to include conversation history
            
        Returns:
            The agent's response
            
        Raises:
            ToolExecutionError: If a tool fails to execute
            AgentRuntimeError: For other runtime errors
        """
        # Build the complete prompt with context and history if needed
        complete_prompt = prompt
        
        if context:
            complete_prompt = f"{context}\n\n{prompt}"
            
        if include_history and self.history:
            history_text = "\n\n".join([
                f"User: {item['user']}\nAgent: {item['agent']}"
                for item in self.history[-5:]  # Include the last 5 exchanges
            ])
            complete_prompt = f"Previous conversation:\n{history_text}\n\nUser: {complete_prompt}"
        
        try:            
            # Execute the agent with the complete prompt
            response = self.agent.run(complete_prompt)
            
            # Update history
            self.history.append({
                "user": prompt,
                "agent": response
            })
            
            return response
            
        except Exception as e:
            raise AgentRuntimeError(
                f"Error running agent: {str(e)}",
                "Check your prompt and try again with more specific instructions"
            )
    
    def get_history(self):
        """Get the conversation history."""
        return self.history
    
    def clear_history(self):
        """Clear the conversation history."""
        self.history = [] 