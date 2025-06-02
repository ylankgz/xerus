# Config.json Customization Guide

This guide will help you understand and customize the `~/.xerus/config.json` file to tailor Xerus to your specific needs, including AI providers, tools, and advanced configurations.

## 📍 Config File Location

Your configuration file is located at:
```bash
~/.xerus/config.json
```

You can edit it with any text editor:
```bash
# Using your preferred editor
code ~/.xerus/config.json
nano ~/.xerus/config.json
vim ~/.xerus/config.json
```

## 🏗️ Configuration Structure

The config.json file has four main sections:

```json
{
  "manager_agent": { /* Main AI agent settings */ },
  "mcpServers": { /* MCP tool servers */ },
  "tools": { /* Built-in and custom tools */ },
  "_example_custom_tool": { /* Example configurations */ }
}
```

## 🤖 Manager Agent Configuration

The manager agent is the main AI that orchestrates all other tools and agents.

### Basic Manager Agent Setup

```json
{
  "manager_agent": {
    "name": "xerus_manager_agent",
    "description": "Your AI assistant for various tasks",
    "model_id": "openai/gpt-4o-mini",
    "api_key": "${OPENAI_API_KEY}",
    "api_base": "https://api.openai.com/v1",
    "parameters": {
      "max_steps": 10,
      "verbosity_level": 2,
      "stream_outputs": true,
      "use_structured_outputs_internally": false
    },
    "code_agent": true
  }
}
```

### Manager Agent Parameters Explained

| Parameter | Description | Default | Options |
|-----------|-------------|---------|---------|
| `max_steps` | Maximum reasoning steps | 10 | 1-50 |
| `verbosity_level` | How much detail to show | 2 | 0 (silent), 1 (minimal), 2 (normal), 3 (verbose) |
| `stream_outputs` | Stream responses in real-time | true | true/false |
| `use_structured_outputs_internally` | Use structured JSON outputs | false | true/false |
| `code_agent` | Enable code execution capabilities | true | true/false |

### Using Different AI Providers

#### OpenAI
```json
{
  "manager_agent": {
    "name": "xerus_manager_agent",
    "description": "AI manager, expert in Python, Data Science, and Machine Learning",
    "model_id": "openai/gpt-4o-mini",
    "api_key": "${OPENAI_API_KEY}",
    "api_base": "https://api.openai.com/v1",
    "parameters": {
      "max_steps": 10,
      "verbosity_level": 2,
      "additional_authorized_imports": [],
      "stream_outputs": true,
      "use_structured_outputs_internally": true
    },
    "code_agent": true
  }
}
```

#### Anthropic Claude
```json
{
  "manager_agent": {
    "name": "xerus_manager_agent",
    "description": "Expert in Data Analytics",
    "model_id": "anthropic/claude-3-sonnet-20240229",
    "api_key": "${ANTHROPIC_API_KEY}",
    "api_base": "https://api.anthropic.com",
    "parameters": {
      "max_steps": 10,
      "verbosity_level": 2,
      "additional_authorized_imports": [],
      "stream_outputs": true,
      "use_structured_outputs_internally": true
    },
    "code_agent": true
  }
}
```

#### Novita (Budget-Friendly)
```json
{
  "web_search_agent": {
    "code_agent": false,
    "name": "web_search_agent",
    "description": "Searches the web for information",
    "tool_class": "smolagents.WebSearchTool",
    "model_id": "novita/meta-llama/llama-4-scout-17b-16e-instruct",
    "api_key": "${NOVITA_API_KEY}",
    "api_base": "https://api.novita.ai/v3/openai",
    "parameters": {
      "max_results": 10,
      "engine": "duckduckgo"
    }
  },
}
```

#### Nebius (Budget-Friendly)
```json
{
  "github": {
    "description": "GitHub MCP server - integrates with GitHub API",
    "_disabled": true,
    "command": "uvx",
    "args": [
      "mcp-server-github"
    ],
    "env": {
      "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
    },
    "model_id": "nebius/meta-llama/Meta-Llama-3.1-8B-Instruct-fast",
    "api_key": "${NEBIUS_API_KEY}",
    "api_base": "https://api.studio.nebius.com/v1"
  }
}
```

## 🛠️ Tools Configuration

The tools section defines individual AI agents that handle specific tasks.

### Built-in Tool Template

```json
{
  "tools": {
    "tool_name_agent": {
      "code_agent": false,
      "name": "tool_name_agent",
      "description": "What this tool does",
      "tool_class": "smolagents.ToolClass",
      "model_id": "provider/model-name",
      "api_key": "${API_KEY}",
      "api_base": "https://api.provider.com/v1",
      "parameters": {
        "tool_specific_param": "value"
      }
    }
  }
}
```

### Available Built-in Tools

#### Web Search Agent
```json
{
  "web_search_agent": {
    "code_agent": false,
    "name": "web_search_agent",
    "description": "Searches the web for information",
    "tool_class": "smolagents.WebSearchTool",
    "model_id": "openai/gpt-4o-mini",
    "api_key": "${OPENAI_API_KEY}",
    "api_base": "https://api.openai.com/v1",
    "parameters": {
      "max_results": 10,
      "engine": "duckduckgo"
    }
  }
}
```

#### Python Interpreter Agent
```json
{
  "python_interpreter_agent": {
    "code_agent": true,
    "name": "python_interpreter_agent", 
    "description": "Executes Python code",
    "tool_class": "smolagents.PythonInterpreterTool",
    "model_id": "openai/gpt-4o-mini",
    "api_key": "${OPENAI_API_KEY}",
    "api_base": "https://api.openai.com/v1",
    "parameters": {
      "authorized_imports": ["math", "random", "datetime", "json", "re", "requests", "pandas", "numpy"]
    }
  }
}
```

#### DuckDuckGo Search Agent
```json
{
  "duckduckgo_search_agent": {
    "code_agent": false,
    "name": "duckduckgo_search_agent",
    "description": "Searches the web using DuckDuckGo",
    "tool_class": "smolagents.DuckDuckGoSearchTool",
    "model_id": "openai/gpt-4o-mini",
    "api_key": "${OPENAI_API_KEY}",
    "api_base": "https://api.openai.com/v1",
    "parameters": {
      "max_results": 10
    }
  }
}
```

#### Webpage Visitor Agent
```json
{
  "visit_webpage_agent": {
    "code_agent": true,
    "name": "visit_webpage_agent",
    "description": "Visits and extracts content from webpages",
    "tool_class": "smolagents.VisitWebpageTool", 
    "model_id": "openai/gpt-4o-mini",
    "api_key": "${OPENAI_API_KEY}",
    "api_base": "https://api.openai.com/v1",
    "parameters": {
      "max_output_length": 40000
    }
  }
}
```

### Creating Custom Tools

#### Simple Function-based Tool

1. **Create your tool file** (`my_custom_tool.py`):
```python
from smolagents import tool

@tool
def calculate_tip(bill_amount: float, tip_percentage: float = 0.18) -> str:
    """Calculate tip amount and total bill.
    
    Args:
        bill_amount: The original bill amount
        tip_percentage: Tip percentage (default 18%)
    
    Returns:
        Formatted string with tip and total
    """
    tip = bill_amount * tip_percentage
    total = bill_amount + tip
    return f"Tip: ${tip:.2f}, Total: ${total:.2f}"
```

2. **Add to config.json**:
```json
{
  "tools": {
    "tip_calculator": {
      "code_agent": false,
      "name": "tip_calculator",
      "description": "Calculates tips and totals for restaurant bills",
      "tool_class": "my_custom_tool.calculate_tip",
      "model_id": "openai/gpt-4o-mini",
      "api_key": "${OPENAI_API_KEY}",
      "api_base": "https://api.openai.com/v1"
    }
  }
}
```

#### Class-based Tool with Parameters

1. **Create your tool file** (`weather_tool.py`):
```python
from smolagents import Tool
import requests

class WeatherTool(Tool):
    def __init__(self, api_key, units="metric", timeout=30):
        super().__init__()
        self.api_key = api_key
        self.units = units
        self.timeout = timeout
    
    @property
    def name(self):
        return "weather_tool"
    
    @property  
    def description(self):
        return "Get current weather for any location"
    
    def forward(self, location: str) -> str:
        """Get weather for a location."""
        # Your weather API implementation here
        return f"Weather in {location}: Sunny, 72°F"
```

2. **Add to config.json**:
```json
{
  "tools": {
    "weather_agent": {
      "code_agent": false,
      "name": "weather_agent",
      "description": "Gets current weather information",
      "tool_class": "weather_tool.WeatherTool",
      "model_id": "openai/gpt-4o-mini",
      "api_key": "${OPENAI_API_KEY}",
      "api_base": "https://api.openai.com/v1",
      "parameters": {
        "api_key": "${WEATHER_API_KEY}",
        "units": "imperial",
        "timeout": 60
      }
    }
  }
}
```

## 🌐 Environment Variables

### Using Environment Variables in Config

Xerus supports environment variable substitution:

| Syntax | Description | Example |
|--------|-------------|---------|
| `${VAR_NAME}` | Required variable | `${OPENAI_API_KEY}` |
| `${VAR_NAME:default}` | Variable with default | `${TIMEOUT:30}` |

### Setting Up Environment Variables

1. **Edit your `.env` file**:
```bash
nano ~/.xerus/.env
```

2. **Add your variables**:
```bash
# AI Provider Keys
OPENAI_API_KEY=sk-your-key-here
ANTHROPIC_API_KEY=sk-ant-your-key-here
NOVITA_API_KEY=your-novita-key
NEBIUS_API_KEY=your-nebius-key

# Custom Tool APIs
WEATHER_API_KEY=your-weather-key
GITHUB_TOKEN=ghp_your-github-token

# Optional Settings
DEFAULT_TIMEOUT=30
DEBUG_MODE=false
```

## 🎯 Advanced Configuration Patterns

### Multi-Provider Setup (Cost Optimization)

Use different providers for different types of tasks:

```json
{
  "manager_agent": {
    "model_id": "openai/gpt-4o-mini",
    "api_key": "${OPENAI_API_KEY}",
    "api_base": "https://api.openai.com/v1"
  },
  "tools": {
    "web_search_agent": {
      "model_id": "novita/meta-llama/llama-4-scout-17b-16e-instruct", 
      "api_key": "${NOVITA_API_KEY}",
      "api_base": "https://api.novita.ai/v3/openai"
    },
    "python_interpreter_agent": {
      "model_id": "anthropic/claude-3-sonnet-20240229",
      "api_key": "${ANTHROPIC_API_KEY}",
      "api_base": "https://api.anthropic.com"
    }
  }
}
```

### Performance-Focused Setup

Use faster models for quick tasks, powerful models for complex ones:

```json
{
  "manager_agent": {
    "model_id": "openai/gpt-4o",
    "api_key": "${OPENAI_API_KEY}",
    "api_base": "https://api.openai.com/v1"
  },
  "tools": {
    "web_search_agent": {
      "model_id": "openai/gpt-4o-mini",
      "api_key": "${OPENAI_API_KEY}",
      "api_base": "https://api.openai.com/v1"
    },
    "python_interpreter_agent": {
      "model_id": "openai/gpt-4o",
      "api_key": "${OPENAI_API_KEY}",
      "api_base": "https://api.openai.com/v1"
    }
  }
}
```

### Budget-Friendly Setup

Use cost-effective providers for all tasks:

```json
{
  "manager_agent": {
    "model_id": "novita/deepseek/deepseek-r1-0528",
    "api_key": "${NOVITA_API_KEY}",
    "api_base": "https://api.novita.ai/v3/openai"
  },
  "tools": {
    "web_search_agent": {
      "model_id": "novita/meta-llama/llama-4-scout-17b-16e-instruct",
      "api_key": "${NOVITA_API_KEY}",
      "api_base": "https://api.novita.ai/v3/openai"
    },
    "python_interpreter_agent": {
      "model_id": "novita/deepseek/deepseek-r1-0528",
      "api_key": "${NOVITA_API_KEY}",
      "api_base": "https://api.novita.ai/v3/openai"
    }
  }
}
```

## 🔧 Troubleshooting Config Issues

### Validating Your Configuration

```bash
# Test your configuration
xerus run --prompt "What tools are available?"

# If there are issues, Xerus will show helpful error messages
```

### Common Configuration Errors

**1. Missing Environment Variables**
```
Error: Environment variable OPENAI_API_KEY not found
```
**Solution**: Add the variable to `~/.xerus/.env`

**2. Invalid JSON Syntax**
```
Error: JSON decode error at line 15
```
**Solution**: Use a JSON validator or editor with syntax checking

**3. Missing Tool Class**
```
Error: Cannot import tool_class 'my_module.MyTool'
```
**Solution**: Ensure the Python file is in your Python path

**4. Invalid Model ID**
```
Error: Model 'invalid/model-name' not found
```
**Solution**: Check the model name with your provider's documentation

### Backup and Restore

**Backup your config**:
```bash
cp ~/.xerus/config.json ~/.xerus/config.json.backup
```

**Restore from backup**:
```bash
cp ~/.xerus/config.json.backup ~/.xerus/config.json
```

**Reset to default**:
```bash
rm ~/.xerus/config.json
xerus init
```

## 📋 Configuration Templates

### Minimal Configuration
```json
{
  "manager_agent": {
    "model_id": "openai/gpt-4o-mini",
    "api_key": "${OPENAI_API_KEY}",
    "api_base": "https://api.openai.com/v1"
  },
  "tools": {
    "python_interpreter_agent": {
      "tool_class": "smolagents.PythonInterpreterTool",
      "model_id": "openai/gpt-4o-mini",
      "api_key": "${OPENAI_API_KEY}",
      "api_base": "https://api.openai.com/v1"
    }
  }
}
```

### Full-Featured Configuration
```json
{
  "manager_agent": {
    "name": "xerus_manager_agent",
    "description": "AI assistant for development and analysis tasks",
    "model_id": "openai/gpt-4o",
    "api_key": "${OPENAI_API_KEY}",
    "api_base": "https://api.openai.com/v1",
    "parameters": {
      "max_steps": 15,
      "verbosity_level": 2,
      "stream_outputs": true,
      "use_structured_outputs_internally": true
    },
    "code_agent": true
  },
  "mcpServers": {
    "filesystem": {
      "command": "uvx",
      "args": ["mcp-server-filesystem", "/Users/username/projects"],
      "description": "File system access"
    },
    "github": {
      "command": "uvx",
      "args": ["mcp-server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
      },
      "description": "GitHub integration"
    }
  },
  "tools": {
    "web_search_agent": {
      "tool_class": "smolagents.WebSearchTool",
      "model_id": "openai/gpt-4o-mini",
      "api_key": "${OPENAI_API_KEY}",
      "api_base": "https://api.openai.com/v1",
      "parameters": {"max_results": 10}
    },
    "python_interpreter_agent": {
      "tool_class": "smolagents.PythonInterpreterTool",
      "model_id": "openai/gpt-4o",
      "api_key": "${OPENAI_API_KEY}",
      "api_base": "https://api.openai.com/v1",
      "parameters": {
        "authorized_imports": ["math", "random", "datetime", "json", "re", "requests", "pandas", "numpy"]
      }
    }
  }
}
```

## 🎨 Best Practices

1. **Start Simple**: Begin with basic configuration and add complexity gradually
2. **Use Environment Variables**: Never hardcode API keys in the config file
3. **Comment Your Changes**: Use `_comment` fields to document your setup
4. **Test Incrementally**: Test each change before adding more
5. **Backup Regularly**: Keep backups of working configurations
6. **Model Selection**: Choose appropriate models for each task type
7. **Resource Management**: Monitor costs and performance with different configurations

## 📚 Further Reading

- [MCP Tools Setup Guide](MCP_SETUP.md) - Setting up external MCP tools
- [Smolagents Documentation](https://huggingface.co/docs/smolagents) - Learn about the underlying agent framework
- [LiteLLM Providers](https://docs.litellm.ai/docs/providers) - Complete list of supported AI providers

---

Happy configuring! 🎉 