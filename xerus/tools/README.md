# Tools Package - Refactored Architecture

This package has been refactored following SOLID principles and object-oriented design patterns to improve maintainability, testability, and extensibility.

## Architecture Overview

The original monolithic `tools.py` file has been broken down into focused, single-responsibility classes:

### Core Classes

#### 🏭 `ToolAgentFactory`
- **Responsibility**: Creating tool agents with specified models and tools
- **Pattern**: Factory Method
- **Location**: `factory.py`

#### 📦 `ToolImporter`
- **Responsibility**: Dynamic importing of tool classes
- **Pattern**: Utility/Helper
- **Location**: `importer.py`

#### 🔗 `MCPServerManager`
- **Responsibility**: Managing MCP server operations and tool loading
- **Pattern**: Manager/Service
- **Location**: `mcp_manager.py`

#### 🛠️ `BuiltInToolsManager`
- **Responsibility**: Managing built-in tools from configuration
- **Pattern**: Manager/Service
- **Location**: `builtin_manager.py`

#### 🎯 `ManagerAgentFactory`
- **Responsibility**: Creating manager agents with all configured tools
- **Pattern**: Factory Method + Composition
- **Location**: `manager_factory.py`

## SOLID Principles Applied

### ✅ Single Responsibility Principle (SRP)
Each class has one clear responsibility:
- `ToolAgentFactory` → Creates tool agents
- `MCPServerManager` → Manages MCP servers
- `BuiltInToolsManager` → Manages built-in tools
- etc.

### ✅ Open/Closed Principle (OCP)
- Easy to extend with new tool types without modifying existing code
- New server types can be added by extending `MCPServerManager`
- New tool sources can be added by creating new manager classes

### ✅ Liskov Substitution Principle (LSP)
- Clear interfaces allow for easy substitution
- Tool factories are interchangeable

### ✅ Interface Segregation Principle (ISP)
- Each class exposes only the methods its clients need
- No fat interfaces forcing unnecessary dependencies

### ✅ Dependency Inversion Principle (DIP)
- High-level modules (ManagerAgentFactory) depend on abstractions
- Dependencies are injected rather than hard-coded

## Usage

### Creating a Manager Agent

```python
from xerus.tools import ManagerAgentFactory

# Create a manager agent with default settings
factory = ManagerAgentFactory()
agent = factory.create_manager_agent()

# Create a manager agent with custom parameters
agent = factory.create_manager_agent(temperature=0.7, max_tokens=1000)
```

### Working with Individual Components

```python
from xerus.tools import MCPServerManager, BuiltInToolsManager, ToolAgentFactory

# Work with MCP tools directly
mcp_manager = MCPServerManager()
mcp_manager.set_server_configs(config)
tools = mcp_manager.load_tools_from_servers()

# Work with built-in tools
builtin_manager = BuiltInToolsManager()
builtin_tools = builtin_manager.load_tools_from_config(config)

# Create individual tool agents
tool_factory = ToolAgentFactory()
agent = tool_factory.create_agent(
    model_id="gpt-4",
    api_key="your-key",
    api_base="https://api.openai.com/v1",
    tools=[tool],
    name="my-tool-agent"
)
```

### Debugging MCP Tools

```python
from xerus.tools import MCPServerManager
from xerus.config import load_config

# List available MCP tools
config = load_config()
mcp_manager = MCPServerManager()
mcp_manager.set_server_configs(config.get('mcpServers', {}))
mcp_manager.list_tools()
```

## Benefits of Refactoring

1. **🔧 Maintainability**: Easier to understand and modify individual components
2. **🧪 Testability**: Each class can be unit tested in isolation
3. **🔄 Reusability**: Components can be reused in different contexts
4. **📈 Extensibility**: Easy to add new features without breaking existing code
5. **🐛 Debugging**: Smaller, focused classes are easier to debug
6. **👥 Team Development**: Multiple developers can work on different components simultaneously

## Design Patterns Used

1. **Factory Method Pattern**: `ToolAgentFactory` and `ManagerAgentFactory` encapsulate object creation
2. **Manager/Service Pattern**: `MCPServerManager` and `BuiltInToolsManager` handle specific domains
3. **Composition Pattern**: `ManagerAgentFactory` composes different managers
4. **Dependency Injection**: Classes receive dependencies rather than creating them

## Extension Examples

### Adding a New Tool Source

```python
from xerus.tools import ToolAgentFactory
from typing import List, Dict, Any
from smolagents import CodeAgent

class CustomToolsManager:
    """Example of extending the architecture with a new tool source."""
    
    def __init__(self):
        self.tool_factory = ToolAgentFactory()
    
    def load_tools_from_custom_source(self, config: Dict[str, Any]) -> List[CodeAgent]:
        # Your custom tool loading logic here
        tools = []  # Load your custom tools
        agents = []
        
        for tool in tools:
            agent = self.tool_factory.create_agent(
                model_id=config["model_id"],
                api_key=config["api_key"],
                api_base=config["api_base"],
                tools=[tool],
                name=f"custom_{tool.name}"
            )
            agents.append(agent)
        
        return agents
```

### Extending MCPServerManager

```python
from xerus.tools import MCPServerManager

class EnhancedMCPServerManager(MCPServerManager):
    """Example of extending MCP server management."""
    
    def create_server_config_with_validation(self, mcp_config: dict):
        # Add custom validation logic
        if not self._validate_config(mcp_config):
            return None
        
        return super().create_server_config(mcp_config)
    
    def _validate_config(self, config: dict) -> bool:
        # Your custom validation logic
        return True
```

## File Structure

```
xerus/tools/
├── __init__.py           # Package entry point
├── factory.py           # ToolAgentFactory
├── importer.py          # ToolImporter  
├── mcp_manager.py       # MCPServerManager
├── builtin_manager.py   # BuiltInToolsManager
├── manager_factory.py   # ManagerAgentFactory
└── README.md           # This file
```

This refactored architecture provides a solid foundation for future development with clean separation of concerns and easy extensibility. 