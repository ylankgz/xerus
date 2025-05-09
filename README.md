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

Enable web search and specific Python packages:

```bash
xerus run "Find the latest SpaceX launch and calculate how many days ago it happened" --tools web_search --imports datetime,math
```

## Features

- Run AI agents from your terminal with simple commands
- Support for various LLM providers (Huggingface, OpenAI, etc.)
- Web search capability through smolagents tools
- Configurable Python package imports for agent code execution
- Rich terminal output with progress indicators

## Command Options

```
Usage: xerus run [OPTIONS] PROMPT

  Run the agent with a prompt.

  PROMPT is the text instruction for the agent to process.

Options:
  --model-type [inference|openai|litellm|transformers]
                                  Type of model to use  [default: inference]
  --model-id TEXT                 ID or name of the model  [default:
                                  Qwen/Qwen2.5-Coder-32B-Instruct]
  --api-key TEXT                  API key for the model service
  --tools TEXT                    Comma-separated list of tools to enable
                                  (e.g., web_search)
  --imports TEXT                  Space-separated list of Python packages to
                                  authorize for import
  --help                          Show this message and exit.
```

## Model Types

- `inference`: Uses Huggingface's InferenceClient (default)
- `openai`: Uses OpenAI API compatible models
- `litellm`: Uses LiteLLM for accessing 100+ LLMs
- `transformers`: Uses local Transformers models

## Example Usage

Search the web and generate a summary:

```bash
xerus run "Summarize the latest news about AI regulation" --tools web_search
```

Use a specific model:

```bash
xerus run "Write a Python script to analyze stock data" --model-type openai --model-id gpt-4 --api-key YOUR_API_KEY
```

Allow specific imports for code execution:

```bash
xerus run "Create a data visualization of the S&P 500 over the last year" --imports pandas,matplotlib,yfinance
```

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