# Xerus Examples

This directory contains examples that demonstrate how to use Xerus CLI with various features.

## Custom Tools

Xerus supports loading custom tools from various sources:

1. **Local file tools** - Create your own tools in Python files
2. **Hugging Face Hub tools** - Load tools from the Hugging Face Hub
3. **Hugging Face Space tools** - Import a Space as a tool
4. **Tool collections** - Load multiple tools at once from a collection

### Example: Using the Hello Tool

`hello_tool.py` provides a simple example of a custom tool that generates greetings in different languages.

```bash
# Run Xerus with the hello_tool
xerus run "Greet me in Spanish" --tool-local ./examples/hello_tool.py
```

### Creating a Custom Tool

To create a custom tool:

1. Import the `Tool` class from `smolagents`
2. Create a class that inherits from `Tool`
3. Define the tool's name, description, inputs, and output type
4. Implement the `forward` method
5. Create an instance of your tool

Example:

```python
from smolagents import Tool

class MyTool(Tool):
    name = "my_tool"
    description = "Description of what the tool does"
    
    inputs = {
        "input_name": {
            "type": "string",
            "description": "Description of the input",
        }
    }
    
    output_type = "string"
    
    def forward(self, input_name: str):
        # Tool implementation
        return f"Processed: {input_name}"

# Create an instance
my_tool = MyTool()
```

### Using Tools from the Hugging Face Hub

You can load tools directly from the Hugging Face Hub:

```bash
xerus run "Analyze sentiment of this text" --tool-hub username/sentiment-tool
```

### Using a Hugging Face Space as a Tool

You can import a Space as a tool using the format `space_id:name:description`:

```bash
xerus run "Generate an image of a mountain landscape" --tool-space stabilityai/stable-diffusion:image_generator:Generates images from text prompts
```

### Using Tool Collections

You can load multiple tools at once from a collection:

```bash
xerus run "Analyze this dataset" --tool-collection huggingface-tools/data-analysis
```

## Combining Multiple Tools

You can combine multiple tools to create more powerful agents:

```bash
xerus run "Find the latest AI research and create a summary" \
  --tools web_search \
  --tool-hub username/summarizer-tool \
  --imports "pandas numpy"
```

This allows the agent to search the web, use a summarization tool, and import pandas and numpy for data analysis. 