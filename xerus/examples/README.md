# Xerus Tool Examples

This directory contains example tools for the Xerus CLI and demonstrates how to create custom tools for your agents.

## Available Example Tools

- **hello_tool.py**: A simple greeting tool that shows basic tool structure
- **calculator_tool.py**: A more complex calculator tool that performs arithmetic operations

## Using the Tools

### From the CLI

You can use these example tools with the Xerus CLI in several ways:

#### 1. Specify a Local Tool File

```bash
xerus run "Say hello to John in Spanish" --tool-local examples/hello_tool.py
```

#### 2. Use the Tools Parameter with File Path

```bash
xerus run "Calculate 5 raised to the power of 3" --tools examples/calculator_tool.py
```

#### 3. Discover Tools from a Directory

```bash
xerus run "Perform calculations and greetings" --tool-dirs examples
```

#### 4. Combine Multiple Tool Sources

```bash
xerus run "Use multiple tools" --tools web_search,examples/calculator_tool.py --tool-dirs examples
```

### In Python Code

You can also use the ToolManager directly in your Python code:

```python
from xerus import ToolManager, create_agent

# Create a tool manager
tool_manager = ToolManager()

# Load tools from various sources
tools = []

# Load from file
local_tools = tool_manager.load_from_local_file("examples/hello_tool.py")
tools.extend(local_tools)

# Load built-in web search tool
web_search = tool_manager.get_tool("web_search")
tools.append(web_search)

# Discover tools from directory
discovered_tools = tool_manager.discover_tools("examples")
tools.extend(discovered_tools)

# Create an agent with these tools
agent = create_agent(
    model_type="inference",
    model_id="Qwen/Qwen2.5-Coder-32B-Instruct",
    tools=tool_manager.get_all_tools()  # or just pass the tools list
)

# Run the agent
response = agent.run("Calculate 5 + 3 and say hello to John in French")
print(response)
```

## Tool Specification Formats

The new tool loading system supports various formats for specifying tools:

- **Built-in tool**: `web_search`
- **Local file**: `path/to/tool.py`
- **HF Hub tool**: `hub:user/repo_id`
- **HF Space tool**: `space:space_id:name:description`
- **HF Collection**: `collection:user/collection_id`

## Creating Your Own Tools

To create a custom tool, follow these steps:

1. Create a Python file with a class that inherits from `smolagents.Tool`
2. Define the required attributes: `name`, `description`, `inputs`, and `output_type`
3. Implement the `forward` method
4. Create an instance of your tool class
5. Use it with Xerus CLI or in your Python code

Example:

```python
from smolagents import Tool

class MyTool(Tool):
    name = "my_tool"
    description = "My custom tool"
    
    inputs = {
        "input1": {
            "type": "string",
            "description": "First input"
        }
    }
    
    output_type = "string"
    
    def forward(self, input1: str):
        return f"Processed: {input1}"

# Create an instance
my_tool = MyTool()

# Test the tool
if __name__ == "__main__":
    result = my_tool(input1="test")
    print(result)  # Output: Processed: test
```

## Tool Discovery

The tool discovery mechanism automatically finds and loads tools from Python files in specified directories. This is useful when you have multiple tools organized in different directories.

Example usage:

```bash
# Discover tools in multiple directories
xerus run "Use discovered tools" --tool-dirs examples,custom_tools,third_party_tools
```

In Python:

```python
from xerus import ToolManager

manager = ToolManager()
tools = []

# Discover tools from multiple directories
for directory in ["examples", "custom_tools", "third_party_tools"]:
    discovered = manager.discover_tools(directory)
    tools.extend(discovered)
``` 