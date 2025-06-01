# Xerus

A command-line interface for running AI agents powered by Huggingface's Smolagents. Xerus lets you interact with powerful language models through a simple CLI, enabling you to perform complex tasks, search the web, and execute code.

## Installation

### Using uv (Recommended)

```bash
uv add xerus-ai
```

### Using pip

```bash
pip install xerus-ai
```

### From source

```bash
# Clone the repository
git clone https://github.com/ylankgz/xerus.git
cd xerus

# Install with uv
uv sync

# Or install with pip
pip install -e .
```

## Getting Started

Before using Xerus, you need to initialize it with an AI provider. Xerus supports multiple providers and makes setup easy with the `init` command.

### Initialize Xerus

Run the initialization command to set up Xerus with your preferred AI provider:

```bash
xerus init
```

This will:
1. Present you with available AI providers
2. Prompt you to enter your API key securely
3. Create configuration files in `~/.xerus/`
4. Set secure permissions on sensitive files

### Supported Providers

Xerus currently supports these AI providers:

#### Nebius
- **Website**: https://studio.nebius.com/
- **API Key Environment Variable**: `NEBIUS_API_KEY`

#### Novita
- **Website**: https://novita.ai/
- **API Key Environment Variable**: `NOVITA_API_KEY`

#### GMI CLoud
- **Website**: https://gmicloud.ai/
- **API Key Environment Variable**: `GMI_CLOUD_API_KEY`


### Quick Setup Examples

**Interactive setup** (recommended for first-time users):
```bash
xerus init
# Follow the prompts to select provider and enter API key
```

**Direct provider selection**:
```bash
xerus init --provider nebius
# Prompts for API key only
```

**Complete non-interactive setup**:
```bash
xerus init --provider novita --api-key YOUR_API_KEY
```

**Force overwrite existing configuration**:
```bash
xerus init --provider nebius --force
```

### Security Features

- **Secure Permissions**: The `.env` file containing your API key is automatically set to `600` permissions (owner read/write only)
- **Hidden Input**: API keys are entered with hidden input for security
- **Environment Detection**: Automatically detects existing API keys in your environment

### What Gets Created

The `init` command creates:

- `~/.xerus/config.json` - Tool configurations and model settings for your chosen provider
- `~/.xerus/.env` - Your API key and other environment variables (with secure 600 permissions)

### Initialization Check

All Xerus commands automatically check if you're properly initialized. If not, you'll see a helpful message:

```
Xerus is not initialized!
Please run the following command to initialize Xerus:
xerus init

This will set up your configuration with an AI provider.
```

## Quick Start

After initializing Xerus, you can start using it immediately:

```bash
xerus run --prompt "What is the current weather in New York City?"
```

Start an interactive chat session:

```bash
xerus chat
```

The manager agent and all tools are configured via `~/.xerus/config.json`. By default, Xerus comes with a comprehensive set of built-in tools including web search, Python code execution, and more.

## Configuration

Xerus uses a flexible configuration system that allows you to customize the manager agent and all tools via a configuration file located at `~/.xerus/config.json`. This eliminates the need to modify any core Xerus code when adding new tools or changing settings.

### Manager Agent Configuration

The manager agent and all tools are now configurable via `~/.xerus/config.json`:

```json
{
  "manager_agent": {
    "name": "xerus_manager_agent",
    "description": "Analyzes, trains, fine-tunes and runs ML models",
    "model_id": "meta-llama/Meta-Llama-3.1-70B-Instruct",
    "api_key": "${NEBIUS_API_KEY}",
    "api_base": "https://api.studio.nebius.ai/v1",
    "parameters": {
      "max_steps": 10,
      "verbosity_level": 2,
      "additional_authorized_imports": ["visit_webpage"],
      "stream_outputs": true,
      "use_structured_outputs_internally": true
    }
  }
}
```

### Tool Configuration

Each tool can be configured with provider-specific settings:

```json
{
  "tools": {
    "web_search_agent": {
      "name": "web_search_agent",
      "description": "Searches the web for information",
      "tool_class": "smolagents.WebSearchTool",
      "model_id": "meta-llama/Meta-Llama-3.1-8B-Instruct",
      "api_key": "${NEBIUS_API_KEY}",
      "api_base": "https://api.studio.nebius.ai/v1",
      "parameters": {
        "max_results": 10,
        "engine": "duckduckgo"
      }
    }
  }
}
```

### Using Different Models and Providers Per Tool

**Xerus allows you to use different models and providers for each tool independently**. This powerful feature lets you optimize performance and cost by choosing the best model for each specific task.

#### How It Works

Each tool in your `~/.xerus/config.json` can have its own:
- `model_id` - Different model for each tool
- `api_key` - Different provider credentials  
- `api_base` - Different API endpoints/providers

#### Example: Mixed Providers and Models

Here's an example showing different providers and models for different tools:

```json
{
  "manager_agent": {
    "name": "xerus_manager_agent", 
    "model_id": "meta-llama/Meta-Llama-3.1-70B-Instruct",
    "api_key": "${NEBIUS_API_KEY}",
    "api_base": "https://api.studio.nebius.ai/v1"
  },
  "tools": {
    "web_search_agent": {
      "name": "web_search_agent",
      "tool_class": "smolagents.WebSearchTool", 
      "model_id": "meta-llama/Meta-Llama-3.1-8B-Instruct",
      "api_key": "${NOVITA_API_KEY}",
      "api_base": "https://api.novita.ai/v3/openai"
    },
    "python_interpreter": {
      "name": "python_interpreter",
      "tool_class": "smolagents.PythonInterpreterTool",
      "model_id": "openai/gpt-4o-mini", 
      "api_key": "${OPENAI_API_KEY}",
      "api_base": "https://api.openai.com/v1"
    },
    "custom_analysis_tool": {
      "name": "data_analyzer",
      "tool_class": "my_tools.DataAnalyzer",
      "model_id": "anthropic/claude-3-sonnet-20240229",
      "api_key": "${ANTHROPIC_API_KEY}", 
      "api_base": "https://api.anthropic.com"
    }
  }
}
```

#### Benefits of Per-Tool Configuration

- **Cost Optimization**: Use cheaper models for simple tasks, premium models for complex ones
- **Performance Tuning**: Match model capabilities to specific tool requirements  
- **Provider Redundancy**: Distribute load across multiple providers
- **Specialized Models**: Use domain-specific models where they excel
- **Fallback Options**: Configure backup providers for reliability

This flexibility allows you to create highly optimized AI agent workflows tailored to your specific needs and budget constraints.

### Environment Variables

Your API keys and other sensitive information are stored in `~/.xerus/.env`:

```bash
# Xerus Environment Configuration for Nebius
# API key for Nebius
NEBIUS_API_KEY=your_api_key_here

# Optional: Add other environment variables here
# GITHUB_TOKEN=your_github_token_here
```

### Universal Parameter System

Xerus features a universal parameter system that allows you to add any tool with any parameters without modifying core code. All parameters from `tools.{tool_name}.parameters` are automatically passed to your tool's `__init__()` method via `**kwargs`.

#### How it Works

1. **Dynamic Import**: The system reads `tool_class` and dynamically imports the tool using `importlib`
2. **Universal Parameter Passing**: All parameters from `tools.{tool_name}.parameters` are passed via `**kwargs`
3. **Automatic Instantiation**: `MyCustomTool(**tool_params)` is called automatically
4. **Error Handling**: If parameters don't match, it falls back gracefully
5. **Zero Code Changes**: Never need to modify any core Xerus files

#### Benefits

- ✅ **Fully Dynamic**: No hardcoded tool mappings
- ✅ **Universal**: Works with any tool from any module  
- ✅ **Zero Touch**: Never edit core Xerus code
- ✅ **Flexible**: Add/remove tools just by editing config
- ✅ **Safe**: Graceful error handling and fallbacks
- ✅ **Future-proof**: Works with tools you haven't written yet

## Extra Parameters

Xerus allows you to pass arbitrary model-specific parameters directly to the underlying model API. This is useful for controlling model behavior such as temperature, top_p, maximum tokens, and other generation settings.

### Using Extra Parameters

You can specify extra parameters by adding them directly after all other options:

```bash
xerus run --prompt "Your prompt" temperature=0.7 top_p=0.95
```

### Parameter Types

The CLI automatically converts parameter values to appropriate Python types:

- **Booleans**: Values like `True` are converted to `True`; values like `False` are converted to `False`
- **Integers**: Numeric values without decimal points are converted to integers
- **Floats**: Numeric values with decimal points are converted to floating-point numbers
- **Strings**: All other values remain as strings

### Common Extra Parameters

Depending on the model type, these are some common parameters you might want to use:

- **temperature**: Controls randomness (higher = more random responses)
- **top_p**: Controls diversity via nucleus sampling
- **max_tokens**: Maximum number of tokens to generate
- **frequency_penalty**: Reduces repetition of token sequences
- **presence_penalty**: Reduces repetition of topics
- **stop**: Custom stop sequences to end generation
- **stream**: Whether to stream responses (boolean)

Example with multiple parameters:

```bash
xerus chat temperature=0.8 max_tokens=1500 presence_penalty=0.5
```

## Features

- Run AI agents from your terminal with simple commands
- Interactive chat mode with conversation history
- Support for various LLM providers (Huggingface, OpenAI, etc.)
- Multiple output formats (rich, plain text, JSON, markdown)
- Built-in tools including:
  - `web_search`: Search the web for information
  - `python_interpreter`: Execute Python code
  - `final_answer`: Provide a final answer to a question
  - `user_input`: Request input from the user
  - `duckduckgo_search`: Search using DuckDuckGo
  - `visit_webpage`: Load and extract content from a webpage
- Load custom tools from various sources:
  - Local Python files
  - Hugging Face Hub
  - Hugging Face Spaces
  - Tool collections
- Rich terminal output with enhanced progress indicators

## Tool Types and Capabilities

Xerus provides a flexible tool system that allows AI agents to interact with various resources. Here's a detailed description of each tool type:

### Built-in Tools
These tools are always available without additional configuration:

- **web_search**: Searches the web for real-time information and returns relevant results
- **python_interpreter**: Executes Python code provided by the agent
- **final_answer**: Allows the agent to provide a definitive answer to the user's query
- **user_input**: Enables the agent to request additional information from the user during execution
- **duckduckgo_search**: Performs targeted searches using the DuckDuckGo search engine API
- **visit_webpage**: Loads and extracts content from a specified URL, allowing the agent to analyze web content

### Creating Custom Tools

You can create your own custom tools for Xerus by writing Python files that contain tool definitions. With the new universal parameter system, you can configure these tools entirely through the configuration file.

#### Basic Custom Tool Example

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

#### Configuration

Add this to your `~/.xerus/config.json`:

```json
{
  "tools": {
    "my_custom_tool": {
      "name": "my_custom_tool",
      "description": "A custom tool that does something amazing",
      "tool_class": "my_custom_tool.MyCustomTool",
      "model_id": "openai/gpt-4o-mini",
      "api_key": "${MY_API_KEY}",
      "api_base": "https://api.myservice.com/v1",
      "parameters": {
        "max_items": 20,
        "api_timeout": 60,
        "debug_mode": true,
        "allowed_domains": ["example.com", "mysite.org"]
      }
    }
  }
}
```

#### Simple Tool with Decorators

For simpler tools, you can use the `@tool` decorator:

```python
# my_tool.py
from smolagents import tool

@tool
def greet(name: str) -> str:
    """Greet a person by name.
    
    Args:
        name: The name of the person to greet
        
    Returns:
        A greeting message
    """
    return f"Hello, {name}! Nice to meet you."
```

#### Advanced Examples

**Using Third-Party Tools:**
```json
{
  "tools": {
    "huggingface_tool": {
      "name": "text_classifier",
      "description": "Classifies text using Hugging Face",
      "tool_class": "transformers.AutoModelForSequenceClassification",
      "model_id": "openai/gpt-4o-mini",
      "api_key": "${API_KEY}",
      "api_base": "https://api.openai.com/v1",
      "parameters": {
        "model_name": "bert-base-uncased",
        "num_labels": 2
      }
    }
  }
}
```

**Using External API Tools:**
```json
{
  "tools": {
    "external_api_tool": {
      "name": "weather_api",
      "description": "Gets weather information",
      "tool_class": "weather_tools.WeatherAPITool",
      "model_id": "openai/gpt-4o-mini",
      "api_key": "${API_KEY}",
      "api_base": "https://api.openai.com/v1",
      "parameters": {
        "api_key": "${WEATHER_API_KEY}",
        "timeout": 30,
        "units": "metric"
      }
    }
  }
}
```

#### No Manual Registry Required!

Just specify the `tool_class` path in your config and you're done!

Key requirements for custom tools:
- Use the `@tool` decorator from smolagents or inherit from the Tool class
- Provide type hints for all parameters and return values
- Include a detailed docstring describing what the tool does and its parameters
- Return values should be JSON-serializable (strings, numbers, booleans, lists, dicts)
- Parameters in the config file will be automatically passed to your tool's constructor

For more complex tools, you can use the Tool class directly:

```python
# advanced_tool.py
from smolagents import Tool

def image_generator(prompt: str) -> str:
    """Generate an image from a text prompt"""
    # Implementation details...
    return "path/to/generated/image.png"

image_tool = Tool(
    name="generate_image",
    description="Generate an image from a text prompt",
    function=image_generator,
    input_schema={"prompt": {"type": "string", "description": "Text prompt for image generation"}}
)
```

After creating your custom tool file, you can use it with Xerus by simply adding it to your configuration file.

## Command Options

With the configuration-based approach, commands are much simpler:

```bash
# Run with a prompt - all configuration from ~/.xerus/config.json
xerus run --prompt "Your prompt here"

# Start interactive chat - all configuration from ~/.xerus/config.json  
xerus chat

# Save sessions with custom names
xerus run --prompt "Your prompt" --session-name "my_analysis"
xerus chat --session-name "research_session"
```

### Commands

```
Usage: xerus [OPTIONS] COMMAND [ARGS]...

Commands:
  init        Initialize Xerus with an AI provider
  run         Run the agent with a prompt
  chat        Start an interactive chat session
  sessions    List all saved sessions
  load        Load and display a saved session
```

#### Init Command

Initialize Xerus with your preferred AI provider:

```bash
xerus init [OPTIONS]
```

Options:
```
  --provider [nebius|novita]  Choose AI provider
  --api-key TEXT              API key for the selected provider (will prompt if not provided)
  --force                     Force overwrite existing configuration
```

Examples:
```bash
# Interactive setup - prompts for provider and API key
xerus init

# Specify provider, prompt for API key
xerus init --provider nebius

# Provide both provider and API key
xerus init --provider novita --api-key YOUR_API_KEY

# Force overwrite existing configuration
xerus init --provider nebius --force
```

#### Run Command

```bash
xerus run --prompt "Your prompt here" [OPTIONS]
```

Additional options:
```
  --prompt TEXT                    Input prompt for the AI model
  --save-session                   Save the session to a file
  --session-name TEXT              Name for this session (used in saved session file)
```

#### Chat Command

```bash
xerus chat [OPTIONS]
```

Additional options:
```
  --session-name TEXT              Name for this session (used in saved session file)
  --no-history                     Don't load or save conversation history
```

#### Session Management

```bash
# List all saved sessions
xerus sessions

# Load and display a saved session
xerus load SESSION_FILE [--output-format FORMAT]
```

## API Key Management

Xerus provides secure and convenient API key management through the `init` command and environment variables.

### Recommended Setup (using xerus init)

The easiest and most secure way to set up API keys is using the `init` command:

```bash
xerus init
```

This will:
- Guide you through provider selection
- Securely prompt for your API key (hidden input)
- Create properly configured files with secure permissions
- Set up environment variable references automatically

### Manual Setup (advanced users)

For manual configuration or when using custom providers, you can also manage API keys through environment variables and `.env` files.

#### Creating a .env file manually

1. Create a `.env` file in `~/.xerus/`:
```bash
# For Nebius
NEBIUS_API_KEY=your_nebius_api_key_here

# For Novita  
NOVITA_API_KEY=your_novita_api_key_here

# For other providers (if using custom configurations)
HF_TOKEN=your_huggingface_token_here
OPENAI_API_KEY=your_openai_key_here
```

2. Secure the file with proper permissions:
```bash
chmod 600 ~/.xerus/.env
```

3. The API keys will be automatically loaded when running Xerus commands.

### Environment Variables

Xerus supports loading environment variables from multiple sources:

1. **System environment variables**
2. **~/.xerus/.env file** (created by `xerus init` or manually)
3. **Project-specific .env file** (if using dotenv in your project)

### Security Best Practices

- **Use `xerus init`**: The recommended approach that handles security automatically
- **File Permissions**: Always ensure `.env` files have `600` permissions (owner read/write only)
- **Version Control**: Never commit `.env` files to version control
- **Environment Variables**: Prefer environment variables over hardcoded keys in configuration files

### Supported Providers

> Note: List of supported providers in LiteLLM [here](https://docs.litellm.ai/docs/providers).

#### Nebius
- Environment Variable: `NEBIUS_API_KEY`
- Website: https://studio.nebius.ai/

#### Novita
- Environment Variable: `NOVITA_API_KEY`  
- Website: https://novita.ai/

#### GMI Cloud
- Environment Variable: `GMI_CLOUD_API_KEY`  
- Website: https://gmicloud.ai/

#### Other Providers (manual configuration)
- Hugging Face: `HF_TOKEN`
- OpenAI: `OPENAI_API_KEY`
- And many more supported by LiteLLM

### Sample .env file

A sample `.env.example` file format:

```bash
# Xerus Environment Configuration
# Choose your provider and add the corresponding API key

# Nebius
NEBIUS_API_KEY=your_nebius_api_key_here

# Novita
NOVITA_API_KEY=your_novita_api_key_here

# Optional: Additional environment variables, required by tools, or MCP servers
GITHUB_TOKEN=your_github_token_here
```

## Example Usages

Search the web and generate a summary:

```bash
xerus run --prompt "Summarize the latest news about AI regulation"
```

Execute Python code directly:

```bash
xerus run --prompt "Calculate the factorial of 10"
```

Search using DuckDuckGo:

```bash
xerus run --prompt "Find information about climate change"
```

Visit and extract content from a webpage:

```bash
xerus run --prompt "Summarize the content from https://huggingface.co/blog"
```

Start an interactive chat session with tools:

```bash
xerus chat --session-name ai_discussion
```

Use custom model parameters:

```bash
xerus run --prompt "Write a creative story" temperature=0.9 top_p=0.95
```

Control model behavior with boolean parameters:

```bash
xerus run --prompt "Translate this to French" use_cache=true stream=false
```

### Linux System Administration

Monitor system resources:

```bash
xerus run --prompt "Check my system's CPU and memory usage, then provide recommendations to optimize performance"
```

Analyze and summarize log files:

```bash
xerus run --prompt "Analyze the last 100 lines of my nginx error logs at /var/log/nginx/error.log and summarize the most common issues"
```

Automate file organization:

```bash
xerus run --prompt "Find all log files in /var/log that are older than 30 days and suggest a command to compress them"
```

Generate shell scripts:

```bash
xerus run --prompt "Create a bash script that backs up my /home/user/projects directory to an external drive, with incremental backups and error logging"
```

### CUDA and GPU Management

Check CUDA configuration:

```bash
xerus run --prompt "Detect CUDA version, installed GPUs, and verify the correct drivers are installed on my system"
```

Optimize GPU workloads:

```bash
xerus run --prompt "Monitor my GPU utilization while running TensorFlow and suggest ways to improve performance"
```

Debug CUDA issues:

```bash
xerus run --prompt "Help me troubleshoot why my PyTorch model is not using my NVIDIA GPU"
```

### Working with Hugging Face

Download and use models:

```bash
xerus run --prompt "Download the BERT base model from Hugging Face and show me how to use it for sentiment analysis on my customer feedback data"
```

Fine-tune models:

```bash
xerus run --prompt "Create a script to fine-tune the Llama-3-8B model on my custom dataset located at ~/data/training_set.json"
```

Deploy models:

```bash
xerus run --prompt "Help me deploy my fine-tuned text classification model to Hugging Face Spaces"
```

### ML Pipelines

Create data processing pipelines:

```bash
xerus run --prompt "Generate a Python script that creates a preprocessing pipeline for my image dataset at ~/datasets/images/ including resizing, augmentation, and normalization"
```

Set up experiment tracking:

```bash
xerus run --prompt "Set up MLflow for tracking experiments on my current machine learning project"
```

Automate model evaluation:

```bash
xerus run --prompt "Create a script to evaluate my trained model against a test dataset and generate precision-recall curves and confusion matrices"
```

Distributed training:

```bash
xerus run --prompt "Help me set up distributed PyTorch training across multiple GPUs on my Linux server"
```

### Log Analysis

Parse and analyze logs:

```bash
xerus run --prompt "Extract all ERROR level logs from my application.log file and categorize them by frequency and type"
```

Create monitoring dashboards:

```bash
xerus run --prompt "Generate a Python script using Plotly to visualize system performance metrics from my collected logs"
```

Set up log rotation:

```bash
xerus run --prompt "Configure logrotate for my application logs to retain 7 days of logs with daily rotation"
```

### Session Management Examples

Save a session:

```bash
xerus run --prompt "Explain quantum physics" --save-session
```

Start a named interactive session:

```bash
xerus chat --session-name physics_study
```

List saved sessions:

```bash
xerus sessions
```

Load a session:

```bash
xerus load physics_study_20230615_123045
```

## Interactive Chat Commands

When in chat mode, you can use the following commands:

- `exit` or `quit`: End the chat session
- `save`: Save the current session

## Local Development

### Using uv (Recommended)

To set up the development environment:

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and setup the project
git clone https://github.com/ylankgz/xerus.git
cd xerus

# Install dependencies and the package in development mode
uv sync --dev

# Run tests
uv run pytest

# Run the CLI
uv run xerus --help

# Or
xerus --help
```

### Using pip

To test the package locally:

```bash
# Install in development mode
pip install -e .
```

## Publishing

### Using uv (Recommended)

Xerus uses modern Python packaging with `pyproject.toml` and uv for fast, reliable builds.

#### Quick Build and Publish

```bash
# Build the package
uv build

# Publish to PyPI (requires PyPI credentials)
uv publish
```

#### Comprehensive Build and Publish Workflow

For a complete workflow with validation and testing:

```bash

# Or step by step:

# 1. Clean previous builds
rm -rf dist/ build/ *.egg-info/

# 2. Install dependencies
uv sync --dev

# 3. Run tests
uv run pytest

# 4. Build package
uv build

# 5. Validate build (optional)
uv run twine check dist/*

# 6. Publish to Test PyPI first (optional)
uv publish --repository testpypi

# 7. Test install from Test PyPI
pip install --index-url https://test.pypi.org/simple/ xerus-ai

# 8. Publish to PyPI
uv publish
```

#### PyPI Authentication

Set up your PyPI credentials for publishing:

```bash
# Option 1: Use environment variables
export UV_PUBLISH_USERNAME="__token__"
export UV_PUBLISH_PASSWORD="pypi-your-token-here"

# Option 2: Use uv auth
uv auth add pypi --username __token__ --password pypi-your-token-here

# Option 3: Use .pypirc file (traditional)
cat > ~/.pypirc << EOF
[distutils]
index-servers = pypi testpypi

[pypi]
username = __token__
password = pypi-your-token-here

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-your-testpypi-token-here
EOF
```

### Using Traditional Tools (pip/build/twine)

If you prefer traditional Python packaging tools:

```bash
# Install build tools
pip install build twine

# Build package
python -m build

# Check build
twine check dist/*

# Upload to PyPI
twine upload dist/*
```

### Release Workflow

For creating releases:

1. **Update version** in `pyproject.toml`
2. **Update CHANGELOG** (if you have one)
3. **Run tests**: `uv run pytest`
4. **Build and publish**: `python scripts/build_and_publish.py`
5. **Create git tag**: `git tag v0.0.7`
6. **Push tag**: `git push origin v0.0.7`
7. **Create GitHub release** (optional)

### Verification

After publishing, verify the package:

```bash
# Create a fresh environment
uv venv test-env
source test-env/bin/activate  # or test-env\Scripts\activate on Windows

# Install from PyPI
pip install xerus-ai

# Test basic functionality
xerus --help
```

Remember to update the version number in `pyproject.toml` before publishing new releases.

## License

This project is licensed under the MIT License - see the LICENSE file for details.