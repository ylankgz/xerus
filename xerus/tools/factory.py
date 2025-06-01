from typing import List, Optional
from smolagents import Tool, CodeAgent

from ..model import ModelFactory
from ..errors import AgentRuntimeError


class ToolAgentFactory:
    """Factory class for creating tool agents with specified models and tools."""
    
    @staticmethod
    def create_agent(
        model_id: str,
        api_key: str,
        api_base: str,
        tools: List[Tool],
        name: Optional[str] = None,
        description: Optional[str] = None,
        **kwargs
    ) -> CodeAgent:
        """
        Create a tool agent with specified model and tools.
        
        Args:
            model_id: ID or name of the model
            api_key: API key for the model service
            api_base: The base URL of the API server
            tools: List of Tool instances
            name: Optional agent name for uniqueness
            description: Optional description of the agent
            **kwargs: Additional arguments for model and agent creation
            
        Returns:
            The initialized CodeAgent
            
        Raises:
            AgentRuntimeError: For agent setup errors
        """
        try:
            tool_model = ModelFactory.create_client(
                model_id=model_id,
                api_key=api_key,
                api_base=api_base,
                **kwargs
            )
            
            agent = CodeAgent(
                tools=tools,
                model=tool_model,
                name=name,
                description=description,
                stream_outputs=True,
                provide_run_summary=True,
                use_structured_outputs_internally=True,
                **kwargs
            )
            return agent
            
        except Exception as e:
            raise AgentRuntimeError(
                f"Failed to initialize tool agent: {e}",
                f"Check model configuration and tool compatibility for tools: {[tool.name for tool in tools]}"
            ) 