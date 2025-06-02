<div align="center">

# Xerus

[![PyPI version](https://badge.fury.io/py/xerus-ai.svg)](https://badge.fury.io/py/xerus-ai)
[![Python](https://img.shields.io/pypi/pyversions/xerus-ai.svg)](https://pypi.org/project/xerus-ai/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://pepy.tech/badge/xerus-ai)](https://pepy.tech/project/xerus-ai)

</div>

A powerful command-line interface for running **CodeAct AI agents** powered by Huggingface's Smolagents. Xerus is an open-source alternative to OpenAI Codex and Claude Code that leverages cheaper open-source models like Deepseek-R1 to generate and execute Python code for your data science, machine learning, and analytics workflows.

**🎯 Designed for Remote Servers**: Xerus is primarily intended for use on your remote development servers, providing a seamless way to perform complex Python tasks, data analysis, and ML operations through natural language commands.

**🔬 CodeAct Methodology**: Built on the [CodeAct research](https://arxiv.org/abs/2402.01030) (first implemented by Manus AI), Xerus agents generate executable Python code as their primary action space, enabling more flexible and powerful automation compared to traditional tool-based approaches.

## 🚀 Quick Start

### Installation

```bash
pip install xerus-ai
```

### Initialize with AI Provider

```bash
xerus init
```

### Try It Out!

```bash
# Data analysis and visualization
xerus run --prompt "Load my CSV dataset and create correlation heatmaps"

# Machine learning workflows  
xerus run --prompt "Train a random forest classifier on my dataset and evaluate performance"

# Start interactive coding session
xerus chat

# Python development and debugging
xerus run --prompt "Optimize this pandas dataframe operation for better performance"

# Search for latest ML techniques
xerus run --prompt "Find the latest research on transformer architectures and summarize"
```

## 📋 Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Why Xerus](#why-xerus)
- [Features](#features)
- [Configuration](#configuration)
- [Commands](#commands)
- [Examples](#examples)
- [Development](#development)
- [License](#license)

## 🤔 Why Xerus?

### **💰 Cost-Effective Alternative**
- Use cheaper open-source models instead of expensive proprietary APIs
- Mix and match different models for different tools based on your needs
- Support for providers like Nebius, Novita, GMI Cloud with competitive pricing

### **🏗️ CodeAct Architecture**  
- Agents generate executable Python code rather than just text responses
- More flexible than pre-defined tool schemas used by other frameworks
- Can compose complex workflows by chaining multiple code executions
- Self-debugging capabilities through iterative code refinement

### **🎛️ Multi-Model Flexibility**
- Use different models for different tasks (e.g., powerful model for complex reasoning, lightweight model for simple operations)
- Connect MCP (Model Context Protocol) servers for extended functionality
- Leverage Huggingface Smolagents for robust agent orchestration

### **🖥️ Remote Server Optimized**
- Designed specifically for headless server environments
- Perfect for data science workstations, ML training servers, and cloud instances
- Terminal-based interface that works seamlessly over SSH

## 📦 Requirements

- Python 3.10+
- An API key from a supported AI provider

## ✨ Features

- **🤖 CodeAct Agents**: Advanced agents that generate and execute Python code
- **💬 Interactive Chat**: Persistent coding sessions with conversation history  
- **🔍 Web Search**: Built-in research capabilities for latest techniques and documentation
- **🐍 Python Execution**: Direct code generation and execution in your environment
- **🔧 Multi-Model Support**: Use different models for different tools and tasks
- **🌐 Multiple Providers**: Support for Nebius, Novita, GMI Cloud, and more open-source model providers
- **📊 Rich Output**: Beautiful terminal output with progress indicators and code syntax highlighting
- **💾 Session Management**: Save and restore your coding sessions
- **🔌 MCP Integration**: Connect Model Context Protocol servers for extended functionality ([MCP Setup Guide](docs/MCP_SETUP.md))

## 🏁 Getting Started

### Step 1: Install Xerus

**Using pip (recommended):**
```bash
pip install xerus-ai
```

**Using uv:**
```bash
uv add xerus-ai
```

### Step 2: Initialize Xerus

Before using Xerus, initialize it with an AI provider:

```bash
xerus init
```

This will:
1. Present you with available AI providers
2. Prompt you to enter your API key securely
3. Create configuration files in `~/.xerus/`
4. Set secure permissions on sensitive files

### Step 3: Start Using Xerus

```bash
# Interactive chat
xerus chat

# One-time prompt
xerus run --prompt "Your question here"
```

### Step 4: Customize Your Setup (Optional)

- **🔧 Advanced Configuration**: See the [Config Customization Guide](docs/CONFIG_CUSTOMIZATION.md) to customize models, tools, and providers
- **🔌 Add MCP Tools**: Follow the [MCP Setup Guide](docs/MCP_SETUP.md) to extend capabilities with file system access, GitHub integration, and more

## 🌟 Supported AI Providers

| Provider | Website | Environment Variable |
|----------|---------|---------------------|
| **Nebius** | [studio.nebius.com](https://studio.nebius.com/) | `NEBIUS_API_KEY` |
| **Novita** | [novita.ai](https://novita.ai/) | `NOVITA_API_KEY` |
| **GMI Cloud** | [gmicloud.ai](https://gmicloud.ai/) | `GMI_CLOUD_API_KEY` |

> See [LiteLLM providers](https://docs.litellm.ai/docs/providers) for the complete list of supported providers.

## 🛠️ Built-in Tools

Xerus comes with powerful built-in tools:

- **`web_search`** - Search the web for real-time information
- **`python_interpreter`** - Execute Python code
- **`duckduckgo_search`** - Search using DuckDuckGo
- **`visit_webpage`** - Load and extract content from URLs
- **`final_answer`** - Provide definitive answers
- **`user_input`** - Request additional information

## 📖 Example Use Cases

### Data Science & Analytics
```bash
# Exploratory data analysis
xerus run --prompt "Load my sales data, identify trends, and create interactive dashboards"

# Statistical analysis and hypothesis testing
xerus run --prompt "Perform A/B testing analysis on my conversion data with statistical significance tests"

# Time series forecasting
xerus run --prompt "Build ARIMA and Prophet models to forecast next quarter's revenue"
```

### Machine Learning & AI
```bash
# Model development and training
xerus run --prompt "Create and train a neural network for image classification using my dataset"

# Hyperparameter optimization  
xerus run --prompt "Set up Optuna hyperparameter tuning for my XGBoost model"

# Model deployment preparation
xerus run --prompt "Convert my PyTorch model to ONNX and create a FastAPI serving endpoint"

# MLOps and monitoring
xerus run --prompt "Set up MLflow experiment tracking and model versioning for my project"
```

### Python Development & Optimization
```bash
# Code optimization and profiling
xerus run --prompt "Profile my pandas pipeline and optimize for memory efficiency"

# Testing and validation
xerus run --prompt "Generate comprehensive unit tests for my data processing functions"

# Documentation and analysis
xerus run --prompt "Analyze my codebase and generate API documentation with usage examples"
```

### Research & Learning
```bash
# Stay updated with latest research
xerus run --prompt "Find and summarize recent papers on transformer efficiency techniques"

# Implementation of research papers
xerus run --prompt "Implement the attention mechanism from the 'Attention Is All You Need' paper"

# Comparative analysis
xerus run --prompt "Compare different optimization algorithms on my dataset and benchmark performance"
```

## 🎯 Command Reference

### Initialize Xerus
```bash
xerus init [--provider PROVIDER] [--api-key KEY] [--force]
```

### Run a Single Prompt
```bash
xerus run --prompt "Your prompt" [--save-session] [--session-name NAME]
```

### Interactive Chat
```bash
xerus chat [--session-name NAME] [--no-history]
```

### Session Management
```bash
xerus sessions          # List all sessions
xerus load SESSION_FILE # Load a session
```

### Model Parameters
You can pass custom parameters to control model behavior:
```bash
xerus run --prompt "Write a story" temperature=0.9 top_p=0.95 max_tokens=1000
```

## ⚙️ Configuration

Xerus uses `~/.xerus/config.json` for configuration. After running `xerus init`, you can customize:

- **Manager agent settings** (model, parameters)
- **Tool configurations** (each tool can use different models/providers)
- **Custom tools** (add your own tools)
- **MCP servers** (connect external tools and services)

For detailed configuration options, see the [Config Customization Guide](docs/CONFIG_CUSTOMIZATION.md).

## 🔒 Python Library Import Configuration

**⚠️ Important Security Note**: Xerus CodeAct agents execute Python code directly on **your machine's operating system** using your **local Python runtime**. This provides powerful capabilities but requires careful security configuration.

### 🛡️ Authorized Imports Security

The `python_interpreter_agent` controls which Python libraries can be imported and executed. This is configured in your `~/.xerus/config.json`:

```json
"python_interpreter_agent": {
  "parameters": {
    "authorized_imports": ["math", "random", "datetime", "json", "re"]
  }
}
```

### 📚 Configuration Options

#### 🔐 **Restricted Mode (Default - Recommended for Local Development)**
```json
"authorized_imports": ["math", "pandas", "numpy", "sklearn", "matplotlib"]
```
- **Safe for local development machines**
- Limits imports to specific, trusted libraries
- Prevents execution of potentially dangerous system operations

#### ⚠️ **Full Access Mode (Use with Extreme Caution)**
```json
"authorized_imports": ["*"]
```
- **⚠️ WARNING: Use ONLY on remote servers or Docker containers**
- Allows importing ANY Python library available in your environment
- Enables full system access, file operations, network requests

### 🏗️ Runtime Environment

Xerus CodeAct agents execute code using:
- **Your machine's operating system** (Linux, macOS, Windows)
- **Your local Python installation** and all installed packages
- **Your user permissions** and file system access
- **Your network connection** and environment variables

> 📖 **For comprehensive security guidelines and configuration examples**, see the [Security & Import Configuration Guide](docs/SECURITY.md).

### Example Configuration
```json
{
  "manager_agent": {
    "model_id": "meta-llama/Meta-Llama-3.1-70B-Instruct",
    "api_key": "${NEBIUS_API_KEY}",
    "api_base": "https://api.studio.nebius.ai/v1"
  },
  "tools": {
    "web_search_agent": {
      "model_id": "meta-llama/Meta-Llama-3.1-8B-Instruct",
      "api_key": "${NOVITA_API_KEY}",
      "api_base": "https://api.novita.ai/v3/openai"
    }
  },
  "mcpServers": {
    "filesystem": {
      "command": "uvx",
      "args": ["mcp-server-filesystem", "/projects"],
      "description": "File system access"
    }
  }
}
```

## 💡 Tips

- **Save important sessions**: Use `--save-session` or `--session-name` to keep track of your work
- **Use specific prompts**: More detailed prompts generally yield better results  
- **Try different providers**: Each provider has different strengths and pricing
- **Experiment with parameters**: Adjust `temperature`, `top_p`, etc. for different behavior
- **Configure for your needs**: Use the [Config Guide](docs/CONFIG_CUSTOMIZATION.md) to optimize your setup
- **Extend with MCP**: Add powerful external tools with [MCP servers](docs/MCP_SETUP.md)

## 🔒 Security

- API keys are stored securely with `600` permissions
- Environment variables are supported for CI/CD
- Hidden input when entering sensitive information
- Configuration files are created in your home directory

## 🚧 Development

### From Source
```bash
git clone https://github.com/ylankgz/xerus.git
cd xerus
uv sync --dev  # or pip install -e .
```

### Running Tests
```bash
uv run pytest  # or pytest
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📚 Documentation

- **[Config Customization Guide](docs/CONFIG_CUSTOMIZATION.md)** - Detailed configuration options
- **[MCP Setup Guide](docs/MCP_SETUP.md)** - Setting up external tools and services

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/ylankgz/xerus/issues)
- **Discussions**: [GitHub Discussions](https://github.com/ylankgz/xerus/discussions)
