# Xerus

A command-line interface for running AI agents powered by Huggingface's Smolagents. Xerus lets you interact with powerful language models through a simple CLI, enabling you to perform complex tasks, search the web, and execute code.

## Installation

```bash
pip install xerus-cli
```

## Quick Start

Run Xerus with a simple prompt:

```bash
xerus run --prompt "What is the current weather in New York City?"
```

Start an interactive chat session:

```bash
xerus chat
```

Enable web search:

```bash
xerus run --prompt "Find the latest SpaceX launch and calculate how many days ago it happened" --built-in-tools
```

Use custom tools:

```bash
# Use a local tool
xerus run --prompt "Generate a greeting" --local-tools ./my_tools.py

# Use a tool from Hugging Face Hub
xerus run --prompt "Analyze sentiment" --hub-tools username/sentiment-tool

# Use a Space as a tool
xerus run --prompt "Generate an image" --space-tools stabilityai/stable-diffusion:image_generator:Generates images from text

# Use Tool Collection as a tool
xerus run --prompt "Draw me a picture of rivers and lakes" --collection-tools huggingface-tools/diffusion-tools-6630bb19a942c2306a2cdb6f
```

Customize model behavior with extra parameters:

```bash
# Control generation with temperature and other parameters
xerus run --prompt "Write me a creative story" temperature=0.9 top_p=0.95
```

## Linux and ML Use Cases

### Linux System Administration

Monitor system resources:

```bash
xerus run --prompt "Check my system's CPU and memory usage, then provide recommendations to optimize performance" --built-in-tools
```

Analyze and summarize log files:

```bash
xerus run --prompt "Analyze the last 100 lines of my nginx error logs at /var/log/nginx/error.log and summarize the most common issues" --built-in-tools
```

Automate file organization:

```bash
xerus run --prompt "Find all log files in /var/log that are older than 30 days and suggest a command to compress them" --built-in-tools
```

Generate shell scripts:

```bash
xerus run --prompt "Create a bash script that backs up my /home/user/projects directory to an external drive, with incremental backups and error logging" --built-in-tools
```

### CUDA and GPU Management

Check CUDA configuration:

```bash
xerus run --prompt "Detect CUDA version, installed GPUs, and verify the correct drivers are installed on my system" --built-in-tools
```

Optimize GPU workloads:

```bash
xerus run --prompt "Monitor my GPU utilization while running TensorFlow and suggest ways to improve performance" --built-in-tools
```

Debug CUDA issues:

```bash
xerus run --prompt "Help me troubleshoot why my PyTorch model is not using my NVIDIA GPU" --built-in-tools
```

### Working with Hugging Face

Download and use models:

```bash
xerus run --prompt "Download the BERT base model from Hugging Face and show me how to use it for sentiment analysis on my customer feedback data" --built-in-tools
```

Fine-tune models:

```bash
xerus run --prompt "Create a script to fine-tune the Llama-3-8B model on my custom dataset located at ~/data/training_set.json" --built-in-tools
```

Deploy models:

```bash
xerus run --prompt "Help me deploy my fine-tuned text classification model to Hugging Face Spaces" --built-in-tools
```

### ML Pipelines

Create data processing pipelines:

```bash
xerus run --prompt "Generate a Python script that creates a preprocessing pipeline for my image dataset at ~/datasets/images/ including resizing, augmentation, and normalization" --built-in-tools
```

Set up experiment tracking:

```bash
xerus run --prompt "Set up MLflow for tracking experiments on my current machine learning project" --built-in-tools
```

Automate model evaluation:

```bash
xerus run --prompt "Create a script to evaluate my trained model against a test dataset and generate precision-recall curves and confusion matrices" --built-in-tools
```

Distributed training:

```bash
xerus run --prompt "Help me set up distributed PyTorch training across multiple GPUs on my Linux server" --built-in-tools
```

### Log Analysis

Parse and analyze logs:

```bash
xerus run --prompt "Extract all ERROR level logs from my application.log file and categorize them by frequency and type" --built-in-tools
```

Create monitoring dashboards:

```bash
xerus run --prompt "Generate a Python script using Plotly to visualize system performance metrics from my collected logs" --built-in-tools
```

Set up log rotation:

```bash
xerus run --prompt "Configure logrotate for my application logs to retain 7 days of logs with daily rotation" --built-in-tools
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
You must install default tools by running `pip install "smolagents[toolkit]"`
These tools are always available without additional configuration:

- **web_search**: Searches the web for real-time information and returns relevant results
- **python_interpreter**: Executes Python code provided by the agent
- **final_answer**: Allows the agent to provide a definitive answer to the user's query
- **user_input**: Enables the agent to request additional information from the user during execution
- **duckduckgo_search**: Performs targeted searches using the DuckDuckGo search engine API
- **visit_webpage**: Loads and extracts content from a specified URL, allowing the agent to analyze web content

### Local Tools

Load custom tools from local Python files:

```bash
xerus run --prompt "Your query" --local-tools ./path/to/tool.py
```

Local tools are Python files that expose one or more tool functions. These files should contain functions decorated with the appropriate Smolagents tool decorators. Local tools run in your local environment and can access local resources.

### Hub Tools

Load tools directly from Hugging Face Hub repositories:

```bash
xerus run --prompt "Your query" --hub-tools username/tool-repository
```

Hub tools are downloaded and executed locally. Always inspect Hub tools before running them, as they execute code in your environment (similar to installing packages via pip/npm).

### Space Tools

Use Hugging Face Spaces as tools:

```bash
xerus run --prompt "Your query" --space-tools username/space-name:tool_name:tool_description
```

Space tools make API calls to deployed Hugging Face Spaces. They provide a way to utilize pre-built, hosted applications as capabilities for your agent.

### Tool Collections

Load multiple tools from a single collection:

```bash
xerus run --prompt "Your query" --collection-tools huggingface-tools/collection-name
```

Tool collections contain multiple pre-configured tools grouped together, allowing your agent to access a suite of related capabilities with a single command.

### Creating Custom Tools

You can create your own custom tools for Xerus by writing Python files that contain tool definitions. Here's a simple example:

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

Key requirements for custom tools:
- Use the `@tool` decorator from smolagents
- Provide type hints for all parameters and return values
- Include a detailed docstring describing what the tool does and its parameters
- Return values should be JSON-serializable (strings, numbers, booleans, lists, dicts)

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

After creating your custom tool file, you can use it with Xerus:

```bash
xerus run --prompt "Generate a greeting for John" --local-tools ./my_tool.py
```

### Tool Specification Formats

When specifying tools to use with Xerus, you can use several different formats:

1. **Built-in Tools**: Use the built-in tools flag
   ```bash
   xerus run --prompt "Search for information" --built-in-tools
   ```

2. **Local File**: Provide the path to a local Python file
   ```bash
   xerus run --prompt "Generate a custom report" --local-tools ./my_tools/report_tool.py
   ```

3. **Hub Tool**: Specify the repository ID
   ```bash
   xerus run --prompt "Analyze sentiment" --hub-tools username/sentiment-analyzer
   ```

4. **Space Tool**: Specify the space ID, tool name, and description
   ```bash
   xerus run --prompt "Generate an image" --space-tools stabilityai/stable-diffusion:image_generator:Creates images from text
   ```

5. **Tool Collection**: Specify the collection slug
   ```bash
   xerus run --prompt "Draw a diagram" --collection-tools huggingface-tools/diagram-tools
   ```

You can combine multiple tool specifications in a single command:
```bash
xerus run --prompt "Research climate change and create a visualization" --built-in-tools --hub-tools username/visualization-tool
```

## Command Options

### Common Options

```
  --model-id TEXT                 ID or name of the model  [default: openai/o4-mini]
  --api-key TEXT                  API key for the model service
  --api-base TEXT                 Custom API base URL
  --built-in-tools                Use built-in tools (web_search, python_interpreter, final_answer, user_input, duckduckgo_search, visit_webpage)
  --local-tools TEXT              Path to a local tool file
  --hub-tools TEXT                Hugging Face Hub repo ID for a tool
  --space-tools TEXT              Hugging Face Space ID to import as a tool
                                  (format: space_id:name:description)
  --collection-tools TEXT         Hugging Face Hub repo ID for a collection of tools
```

### Commands

```
Usage: xerus [OPTIONS] COMMAND [ARGS]...

Commands:
  run         Run the agent with a prompt
  chat        Start an interactive chat session
  sessions    List all saved sessions
  load        Load and display a saved session
```

#### Run Command

```bash
xerus run --prompt "Your prompt here" [OPTIONS]
```

Additional options:
```
  --prompt TEXT                    Input prompt for the AI model
  --model-id TEXT                  ID or name of the model  [default: openai/o4-mini]
  --api-key TEXT                   API key for the model service
  --api-base TEXT                  Custom API base URL
  --custom-role-conversions TEXT   Path to JSON file with role conversions
  --flatten-messages-as-text       Flatten messages to plain text
  --built-in-tools                 Use built-in tools (web_search, python_interpreter, final_answer, user_input, duckduckgo_search, visit_webpage)
  --local-tools TEXT               Path to local tool file
  --hub-tools TEXT                 List of HuggingFace Hub repos
  --space-tools TEXT               List of HuggingFace Spaces (format: space_id:name:description)
  --collection-tools TEXT          HuggingFace Hub repo ID for a collection of tools
  --save-session                   Save this session to a file for later reference
```

#### Chat Command

```bash
xerus chat [OPTIONS]
```

Additional options:
```
  --model-id TEXT                  ID or name of the model  [default: openai/o4-mini]
  --api-key TEXT                   API key for the model service
  --api-base TEXT                  Custom API base URL
  --custom-role-conversions TEXT   Path to JSON file with role conversions
  --flatten-messages-as-text       Flatten messages to plain text
  --built-in-tools                 Use built-in tools (web_search, python_interpreter, final_answer, user_input, duckduckgo_search, visit_webpage)
  --local-tools TEXT               Path to local tool file
  --hub-tools TEXT                 List of HuggingFace Hub repos
  --space-tools TEXT               List of HuggingFace Spaces (format: space_id:name:description)
  --collection-tools TEXT          HuggingFace Hub repo ID for a collection of tools
  --no-history                     Don't load or save conversation history
  --session-name TEXT              Name for this session (used in saved session file)
```

#### Session Management

```bash
# List all saved sessions
xerus sessions

# Load and display a saved session
xerus load SESSION_FILE [--output-format FORMAT]
```

## API Key Management

For securely storing API keys across terminal sessions, Xerus supports loading environment variables from a `.env` file. This is especially useful for remote servers or when you need persistent configuration.

### Setting up environment variables with dotenv

1. Create a `.env` file in your project root:
```bash
# For Hugging Face models (default)
HF_TOKEN=your_huggingface_token_here
# For LiteLLM models
LITELLM_API_KEY=your_litellm_key_here
```
> Note: List of supported providers in LiteLLM [here](https://docs.litellm.ai/docs/providers).

2. Secure the file with proper permissions:
```bash
chmod 600 .env
```

3. Add to your `.gitignore` to prevent accidental commits:
```bash
echo ".env" >> .gitignore
```

The appropriate environment variables will be automatically loaded when running Xerus commands, allowing you to omit the `--api-key` parameter.

### Sample .env file

A sample `.env.example` file is included in the repository. You can copy it to create your own configuration:

```bash
cp .env.example .env
```

Then edit the `.env` file to add your API keys.

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
xerus chat --model-id gpt-4 --api-key YOUR_API_KEY temperature=0.8 max_tokens=1500 presence_penalty=0.5
```

## Example Usage

Search the web and generate a summary:

```bash
xerus run --prompt "Summarize the latest news about AI regulation" --built-in-tools
```

Execute Python code directly:

```bash
xerus run --prompt "Calculate the factorial of 10" --built-in-tools
```

Search using DuckDuckGo:

```bash
xerus run --prompt "Find information about climate change" --built-in-tools
```

Visit and extract content from a webpage:

```bash
xerus run --prompt "Summarize the content from https://huggingface.co/blog" --built-in-tools
```

Start an interactive chat session with tools:

```bash
xerus chat --built-in-tools --session-name ai_discussion
```

Use custom model parameters:

```bash
xerus run --prompt "Write a creative story" temperature=0.9 top_p=0.95
```

Run model with specific generation parameters:

```bash
xerus chat --model-id gpt-4 --api-key YOUR_API_KEY temperature=0.7 max_tokens=2000
```

Control model behavior with boolean parameters:

```bash
xerus run --prompt "Translate this to French" use_cache=true stream=false
```

Get output in JSON format:

```bash
xerus run --prompt "What are the top 5 programming languages in 2023?"
```

Use a specific model:

```bash
xerus run --prompt "Write a Python script to analyze stock data" --model-id gpt-4 --api-key YOUR_API_KEY
```

### Using Custom Tools

Create a custom greeting tool:

```bash
xerus run --prompt "Say hello to me in Spanish" --local-tools ./examples/hello_tool.py
```

Use an image generation tool from Hugging Face Space:

```bash
xerus run --prompt "Generate an image of a sunset over mountains" --space-tools stabilityai/stable-diffusion:image_generator:Creates images from text prompts
```

Combine multiple tools:

```bash
xerus run --prompt "Find news about climate change and generate an infographic" --built-in-tools --hub-tools username/infographic-tool
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
- `history`: View conversation history
- `clear`: Clear the conversation history
- `save`: Save the current session

## Local Development

To test the package locally:

```bash
# Install in development mode
pip install -e .
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Publishing

To build and publish your package, you can run:

```bash
pip install build twine
python -m build
python -m twine upload dist/*
```

Remember to update the package information in setup.py with your actual details before publishing.