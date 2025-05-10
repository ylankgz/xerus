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

## Features

- Run AI agents from your terminal with simple commands
- Interactive chat mode with conversation history
- Support for various LLM providers (Huggingface, OpenAI, etc.)
- Multiple output formats (rich, plain text, JSON, markdown)
- Web search capability through smolagents tools
- Session management with save, load, and list capabilities
- Load custom tools from various sources:
  - Local Python files
  - Hugging Face Hub
  - Hugging Face Spaces
  - Tool collections
- Configurable Python package imports for agent code execution
- Rich terminal output with enhanced progress indicators

## Command Options

### Common Options

```
  --model-type [inference|openai|azure-openai|amazon-bedrock|litellm|transformers|mlx-lm]
                                  Type of model to use  [default: inference]
  --model-id TEXT                 ID or name of the model  [default:
                                  Qwen/Qwen2.5-Coder-32B-Instruct]
  --api-key TEXT                  API key for the model service
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
xerus run "Your prompt" --model-type openai --model-id gpt-4 --api-key YOUR_KEY
```
- **Environment variable**: `OPENAI_API_KEY`
- **Key parameters**:
  - `--model-id`: Model name (e.g., "gpt-4", "gpt-3.5-turbo")
  - `--api-key`: OpenAI API key
  - `--api-base`: Optional custom API endpoint

### litellm
Gateway to 100+ LLMs through LiteLLM.
```bash
xerus run "Your prompt" --model-type litellm --model-id anthropic/claude-3-5-sonnet-latest
```
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
- **Key parameters**:
  - `--model-id`: Model ID on Hugging Face Hub
  - `--device-map`: Device to run model on (e.g., "auto", "cpu")
  - `--trust-remote-code`: Whether to trust remote code (boolean flag)

### mlx-lm
Optimized for Apple Silicon using the MLX framework.
```bash
xerus run "Your prompt" --model-type mlx-lm --model-id HuggingFaceTB/SmolLM-135M-Instruct
```
- **Key parameters**:
  - `--model-id`: MLX-compatible model ID

## Example Usage

Search the web and generate a summary:

```bash
xerus run "Summarize the latest news about AI regulation" --tools web_search
```

Start an interactive chat session with web search:

```bash
xerus chat --tools web_search --session-name ai_discussion
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