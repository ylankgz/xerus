# Custom Tool Parameter Example

This example shows how the universal parameter system works in Xerus, allowing you to add any tool with any parameters without modifying any core code.

## Example Custom Tool

```python
# my_custom_tool.py
from smolagents import Tool

class MyCustomTool(Tool):
    def __init__(self, max_items=10, api_timeout=30, debug_mode=False, allowed_domains=None):
        super().__init__()
        self.max_items = max_items
        self.api_timeout = api_timeout  
        self.debug_mode = debug_mode
        self.allowed_domains = allowed_domains or []
        
    @property
    def name(self):
        return "my_custom_tool"
        
    @property  
    def description(self):
        return "A custom tool that does something amazing"
        
    def forward(self, query: str) -> str:
        if self.debug_mode:
            print(f"Debug: Processing query with max_items={self.max_items}")
        
        # Your tool logic here
        return f"Processed: {query}"
```

## Configuration

Add this to your `~/.xerus/config.toml`:

```toml
[tools.my_custom_tool]
name = "my_custom_tool"
description = "A custom tool that does something amazing"
tool_class = "my_custom_tool.MyCustomTool"  # Module.ClassName path
model_id = "openai/gpt-4o-mini"
api_key = "${MY_API_KEY}"
api_base = "https://api.myservice.com/v1"

# These parameters will be automatically passed to MyCustomTool.__init__()
[tools.my_custom_tool.parameters]
max_items = 20
api_timeout = 60
debug_mode = true
allowed_domains = ["example.com", "mysite.org"]
```

## How it Works

1. **Dynamic Import**: The system reads `tool_class` and dynamically imports the tool using `importlib`
2. **Universal Parameter Passing**: All parameters from `[tools.{tool_name}.parameters]` are passed via `**kwargs`
3. **Automatic Instantiation**: `MyCustomTool(**tool_params)` is called automatically
4. **Error Handling**: If parameters don't match, it falls back gracefully
5. **Zero Code Changes**: Never need to modify any core Xerus files

## Benefits

- ✅ **Fully Dynamic**: No hardcoded tool mappings
- ✅ **Universal**: Works with any tool from any module  
- ✅ **Zero Touch**: Never edit core Xerus code
- ✅ **Flexible**: Add/remove tools just by editing config
- ✅ **Safe**: Graceful error handling and fallbacks
- ✅ **Future-proof**: Works with tools you haven't written yet

## Advanced Examples

### Using Third-Party Tools
```toml
[tools.huggingface_tool]
name = "text_classifier"
description = "Classifies text using Hugging Face"
tool_class = "transformers.AutoModelForSequenceClassification"
model_id = "openai/gpt-4o-mini"
api_key = "${API_KEY}"
api_base = "https://api.openai.com/v1"

[tools.huggingface_tool.parameters]
model_name = "bert-base-uncased"
num_labels = 2
```

### Using Tools from Different Modules
```toml
[tools.external_api_tool]
name = "weather_api"
description = "Gets weather information"
tool_class = "weather_tools.WeatherAPITool"
model_id = "openai/gpt-4o-mini"
api_key = "${API_KEY}"
api_base = "https://api.openai.com/v1"

[tools.external_api_tool.parameters]
api_key = "${WEATHER_API_KEY}"
timeout = 30
units = "metric"
```

## No Manual Registry Required!

Unlike the old system, you **never** need to:
- ❌ Edit `tools.py` 
- ❌ Add imports for new tools
- ❌ Update tool class mappings
- ❌ Modify core Xerus code

Just specify the `tool_class` path in your config and you're done! 🎉 