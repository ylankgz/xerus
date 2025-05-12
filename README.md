# Xerus

A command-line interface for running AI agents powered by Huggingface's Smolagents. Xerus lets you interact with powerful language models through a simple CLI, enabling you to perform complex tasks, search the web, and execute code.

## Installation

```bash
pip install xerus
```

## Quick Start

Run Xerus with a simple prompt:

```bash
xerus run "What is the current weather in New York City?"
```

Start an interactive chat session:

```bash
xerus chat
```

Enable web search and specific Python packages:

```bash
xerus run "Find the latest SpaceX launch and calculate how many days ago it happened" --tools web_search --imports datetime,math
```

Use custom tools:

```bash
# Use a local tool
xerus run "Generate a greeting" --tool-local ./my_tools.py

# Use a tool from Hugging Face Hub
xerus run "Analyze sentiment" --tool-hub username/sentiment-tool

# Use a Space as a tool
xerus run "Generate an image" --tool-space stabilityai/stable-diffusion:image_generator:Generates images from text

# Use Tool Collection as a tool
xerus run "Draw me a picture of rivers and lakes" --tool-space huggingface-tools/diffusion-tools-6630bb19a942c2306a2cdb6f
```

Customize model behavior with extra parameters:

```bash
# Control generation with temperature and other parameters
xerus run "Write me a creative story" --extra-params="temperature=0.9" --extra-params="top_p=0.95"
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
  - `google_search`: Search using Google
  - `visit_webpage`: Load and extract content from a webpage
- Load custom tools from various sources:
  - Local Python files
  - Hugging Face Hub
  - Hugging Face Spaces
  - Tool collections
- Configurable Python package imports for agent code execution
- Rich terminal output with enhanced progress indicators

## Tool Types and Capabilities

Xerus provides a flexible tool system that allows AI agents to interact with various resources. Here's a detailed description of each tool type:

### Built-in Tools
You must install default tools by running `pip install "smolagents[toolkit]"`
These tools are always available without additional configuration:

- **web_search**: Searches the web for real-time information and returns relevant results
- **python_interpreter**: Executes Python code provided by the agent, with configurable package imports
- **final_answer**: Allows the agent to provide a definitive answer to the user's query
- **user_input**: Enables the agent to request additional information from the user during execution
- **duckduckgo_search**: Performs targeted searches using the DuckDuckGo search engine API
- **visit_webpage**: Loads and extracts content from a specified URL, allowing the agent to analyze web content

### Local Tools

Load custom tools from local Python files:

```bash
xerus run "Your query" --tool-local ./path/to/tool.py
```

Local tools are Python files that expose one or more tool functions. These files should contain functions decorated with the appropriate Smolagents tool decorators. Local tools run in your local environment and can access local resources.

### Hub Tools

Load tools directly from Hugging Face Hub repositories:

```bash
xerus run "Your query" --tool-hub username/tool-repository
```

Hub tools are downloaded and executed locally. Always inspect Hub tools before running them, as they execute code in your environment (similar to installing packages via pip/npm).

### Space Tools

Use Hugging Face Spaces as tools:

```bash
xerus run "Your query" --tool-space username/space-name:tool_name:tool_description
```

Space tools make API calls to deployed Hugging Face Spaces. They provide a way to utilize pre-built, hosted applications as capabilities for your agent.

### Tool Collections

Load multiple tools from a single collection:

```bash
xerus run "Your query" --tool-collection huggingface-tools/collection-name
```

Tool collections contain multiple pre-configured tools grouped together, allowing your agent to access a suite of related capabilities with a single command.

### Tool Discovery

You can automatically discover and load tools from specified directories:

```bash
xerus run "Your query" --tool-dirs ./my_tools,./more_tools
```

This scans the specified directories for Python files containing tool definitions and makes them available to your agent.

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
xerus run "Generate a greeting for John" --tool-local ./my_tool.py
```

### Tool Specification Formats

When specifying tools to use with Xerus, you can use several different formats:

1. **Built-in Tools**: Simply use the tool name
   ```bash
   xerus run "Search for information" --tools web_search,python_interpreter
   ```

2. **Local File**: Provide the path to a local Python file
   ```bash
   xerus run "Generate a custom report" --tool-local ./my_tools/report_tool.py
   ```

3. **Hub Tool**: Use the `hub:` prefix followed by the repository ID
   ```bash
   xerus run "Analyze sentiment" --tool-hub username/sentiment-analyzer
   ```

4. **Space Tool**: Use the `space:` prefix followed by the space ID, optional tool name, and description
   ```bash
   xerus run "Generate an image" --tool-space stabilityai/stable-diffusion:image_generator:Creates images from text
   ```

5. **Tool Collection**: Use the `collection:` prefix followed by the collection slug
   ```bash
   xerus run "Draw a diagram" --tool-collection huggingface-tools/diagram-tools
   ```

You can combine multiple tool specifications in a single command:
```bash
xerus run "Research climate change and create a visualization" --tools web_search,python_interpreter --tool-hub username/visualization-tool --imports matplotlib,pandas
```

## Command Options

### Common Options

```
  --model-type [inference|openai|litellm|transformers|mlx-lm]
                                  Type of model to use  [default: inference]
  --model-id TEXT                 ID or name of the model  [default:
                                  Qwen/Qwen2.5-Coder-32B-Instruct]
  --api-key TEXT                  API key for the model service
  --extra-params TEXT             Extra parameters in key=value format (can be specified multiple times).
                                  Example: --extra-params="temperature=0.7" --extra-params="top_p=0.9"
  --tools TEXT                    Comma-separated list of tools to enable
                                  (e.g., web_search)
  --imports TEXT                  Space-separated list of Python packages to
                                  authorize for import
  --tool-local TEXT               Path to a local tool file
  --tool-hub TEXT                 Hugging Face Hub repo ID for a tool
  --tool-space TEXT               Hugging Face Space ID to import as a tool
                                  (format: space_id:name:description)
  --tool-collection TEXT          Hugging Face Hub repo ID for a collection of tools
  --tool-dirs TEXT                Comma-separated list of directories to discover tools from
  --output-format [rich|plain|json|markdown]
                                  Output format  [default: rich]
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
xerus run "Your prompt here" [OPTIONS]
```

Additional options:
```
  --save-session                   Save this session to a file for later reference
```

#### Chat Command

```bash
xerus chat [OPTIONS]
```

Additional options:
```
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

# For OpenAI Compatible models
OPENAI_API_KEY=your_openai_key_here

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

## Model Types

Xerus supports multiple model types through different backends. Configure them using `--model-type` and appropriate parameters:

### inference
Default model type using Hugging Face's InferenceClient.
```bash
xerus run "Your prompt" --model-type inference --model-id Qwen/Qwen2.5-Coder-32B-Instruct
```
- **Environment variable**: `HF_TOKEN`
- **Default model**: Qwen/Qwen2.5-Coder-32B-Instruct
- **Key parameters**:
  - `--model-id`: Model ID on Hugging Face Hub
  - `--api-key`: HF token (or use HF_TOKEN env var)
  

### openai
Uses OpenAI API compatible models.
```bash
xerus run "Your prompt" --model-type openai --model-id o4-mini --api-key YOUR_KEY
```
- **Requirements**: You must have `openai` installed. You can install it by running `pip install "smolagents[openai]"`
- **Environment variable**: `OPENAI_API_KEY`
- **Key parameters**:
  - `--model-id`: Model name (e.g., "gpt-4", "gpt-3.5-turbo")
  - `--api-key`: OpenAI API key
  - `--api-base`: Optional custom API endpoint

### litellm
Gateway to 100+ LLMs through LiteLLM.
```bash
xerus run "Your prompt" --model-type litellm --model-id anthropic/claude-3-7-sonnet-latest
```
- **Requirements**: You must install LiteLLM by running `pip install "smolagents[litellm]"`
- **Environment variable**: `LITELLM_API_KEY`
- **Key parameters**:
  - `--model-id`: LiteLLM model identifier
  - `--api-key`: LiteLLM API key
  - `--api-base`: Optional custom API endpoint

### transformers
Runs models locally using the Transformers library.
```bash
xerus run "Your prompt" --model-type transformers --model-id mistralai/Mistral-7B-Instruct-v0.2
```
- **Requirements**: You must have `transformers` and `torch` installed. You can run command `pip install smolagents[transformers]`
- **Key parameters**:
  - `--model-id`: Model ID on Hugging Face Hub
  - `--device-map`: Device to run model on (e.g., "auto", "cpu")
  - `--trust-remote-code`: Whether to trust remote code (boolean flag)

### mlx-lm
Optimized for Apple Silicon using the MLX framework.
```bash
xerus run "Your prompt" --model-type mlx-lm --model-id HuggingFaceTB/SmolLM-135M-Instruct
```
- **Requirements**: Apple Silicon Mac with `mlx` and `mlx-lm` installed. You can install it by running `pip install "smolagents[mlx-lm]"`
- **Key parameters**:
  - `--model-id`: MLX-compatible model ID

## Extra Parameters

Xerus allows you to pass arbitrary model-specific parameters directly to the underlying model API. This is useful for controlling model behavior such as temperature, top_p, maximum tokens, and other generation settings.

### Using Extra Parameters

You can specify extra parameters in key=value format using the `--extra-params` option. This option can be used multiple times to set different parameters:

```bash
xerus run "Your prompt" --extra-params="temperature=0.7" --extra-params="top_p=0.95"
```

### Parameter Types

The CLI automatically converts parameter values to appropriate Python types:

- **Booleans**: Values like `true`, `yes`, `y`, `1` are converted to `True`; values like `false`, `no`, `n`, `0` are converted to `False`
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
xerus chat --model-type openai --model-id gpt-4 --extra-params="temperature=0.8" --extra-params="max_tokens=1500" --extra-params="presence_penalty=0.5"
```

## Example Usage

Search the web and generate a summary:

```bash
xerus run "Summarize the latest news about AI regulation" --tools web_search
```

Execute Python code directly:

```bash
xerus run "Calculate the factorial of 10" --tools python_interpreter
```

Use Google search specifically:

```bash
xerus run "Find information about climate change" --tools google_search
```

Visit and extract content from a webpage:

```bash
xerus run "Summarize the content from https://huggingface.co/blog" --tools visit_webpage
```

Start an interactive chat session with web search:

```bash
xerus chat --tools web_search,python_interpreter --session-name ai_discussion
```

Use custom model parameters:

```bash
xerus run "Write a creative story" --extra-params="temperature=0.9" --extra-params="top_p=0.95"
```

Run model with specific generation parameters:

```bash
xerus chat --model-type openai --model-id gpt-4 --extra-params="temperature=0.7" --extra-params="max_tokens=2000"
```

Control model behavior with boolean parameters:

```bash
xerus run "Translate this to French" --extra-params="use_cache=true" --extra-params="stream=false"
```

Get output in JSON format:

```bash
xerus run "What are the top 5 programming languages in 2023?" --output-format json
```

Use a specific model:

```bash
xerus run "Write a Python script to analyze stock data" --model-type openai --model-id gpt-4 --api-key YOUR_API_KEY
```

Allow specific imports for code execution:

```bash
xerus run "Create a data visualization of the S&P 500 over the last year" --imports pandas,matplotlib,yfinance
```

### Using Custom Tools

Create a custom greeting tool:

```bash
xerus run "Say hello to me in Spanish" --tool-local ./examples/hello_tool.py
```

Use an image generation tool from Hugging Face Space:

```bash
xerus run "Generate an image of a sunset over mountains" --tool-space stabilityai/stable-diffusion:image_generator:Creates images from text prompts
```

Combine multiple tools:

```bash
xerus run "Find news about climate change and generate an infographic" --tools web_search --tool-hub username/infographic-tool --imports matplotlib,pandas
```

### Session Management Examples

Save a session:

```bash
xerus run "Explain quantum physics" --save-session
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

See the `examples` directory for more detailed examples and tool templates.

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