# MCP Tools Setup Guide

This guide will help you set up MCP (Model Context Protocol) tools in Xerus to extend your AI agent's capabilities with powerful external tools and services.

## 🤔 What is MCP?

MCP (Model Context Protocol) is a standard that allows AI agents to connect to external tools and services. Think of it as a way to give your AI agent "superpowers" by connecting it to:

- **File systems** - Read, write, and manage files
- **APIs** - Connect to GitHub, databases, web services
- **Development tools** - Git operations, code analysis
- **System tools** - Command execution, system monitoring

## 🚀 Quick Start

### 1. Initialize Xerus (if not done already)

```bash
xerus init
```

### 2. Install MCP Tools

Most MCP tools can be installed using `uvx`:

```bash
# Install filesystem access
uvx install mcp-server-filesystem

# Install GitHub integration
uvx install mcp-server-github

# Install SQLite database tools
uvx install mcp-server-sqlite
```

### 3. Configure MCP Tools

Edit your `~/.xerus/config.json` file and add MCP servers:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "uvx",
      "args": ["mcp-server-filesystem", "/Users/username/projects"],
      "description": "File system access to projects folder"
    }
  }
}
```

### 4. Test Your Setup

```bash
xerus run --prompt "List all files in my projects directory"
```

## 🛠️ MCP Server Types

Xerus supports two types of MCP servers:

### Stdio Servers (Local Tools)
- **How they work**: Run as local processes communicating via stdin/stdout
- **Use case**: File system access, local development tools, system utilities
- **Security**: Higher permissions (can access your local system)

### HTTP Servers (Remote Services)
- **How they work**: Connect to running web services via HTTP
- **Use case**: Web APIs, cloud services, remote databases
- **Security**: Lower risk (no local system access)

## 📋 Popular MCP Tools

### 🗂️ File System Access

**Purpose**: Read, write, and manage files safely
**Installation**:
```bash
uvx install mcp-server-filesystem
```

**Configuration**:
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "uvx",
      "args": ["mcp-server-filesystem", "/Users/username/projects"],
      "description": "Safe file system access to projects directory"
    }
  }
}
```

**Example Usage**:
```bash
xerus run --prompt "Create a new Python project structure with main.py, requirements.txt, and README.md"
xerus run --prompt "Find all Python files in my project and show me which ones need docstrings"
```

### 🐙 GitHub Integration

**Purpose**: Manage GitHub repositories, issues, pull requests
**Installation**:
```bash
uvx install mcp-server-github
```

**Setup Environment Variables**:
```bash
# Add to ~/.xerus/.env
GITHUB_TOKEN=your_github_personal_access_token
```

**Configuration**:
```json
{
  "mcpServers": {
    "github": {
      "command": "uvx",
      "args": ["mcp-server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
      },
      "description": "GitHub API integration"
    }
  }
}
```

**Example Usage**:
```bash
xerus run --prompt "Create a new GitHub repository for my ML project with appropriate labels and initial structure"
xerus run --prompt "Check the open issues in my repository and suggest which ones to prioritize"
```

### 🗃️ SQLite Database

**Purpose**: Query and manage SQLite databases
**Installation**:
```bash
uvx install mcp-server-sqlite
```

**Configuration**:
```json
{
  "mcpServers": {
    "database": {
      "command": "uvx",
      "args": ["mcp-server-sqlite", "/path/to/your/database.db"],
      "description": "SQLite database access"
    }
  }
}
```

**Example Usage**:
```bash
xerus run --prompt "Analyze my database schema and suggest optimizations"
xerus run --prompt "Create a query to find users who haven't logged in for 30 days"
```

### 📱 Appwrite Backend

**Purpose**: Integrate with Appwrite backend services
**Installation**:
```bash
uvx install mcp-server-appwrite
```

**Setup Environment Variables**:
```bash
# Add to ~/.xerus/.env
APPWRITE_PROJECT_ID=your_project_id
APPWRITE_API_KEY=your_api_key
APPWRITE_ENDPOINT=https://cloud.appwrite.io/v1  # optional
```

**Configuration**:
```json
{
  "mcpServers": {
    "appwrite": {
      "command": "uvx",
      "args": ["mcp-server-appwrite"],
      "env": {
        "APPWRITE_PROJECT_ID": "${APPWRITE_PROJECT_ID}",
        "APPWRITE_API_KEY": "${APPWRITE_API_KEY}",
        "APPWRITE_ENDPOINT": "${APPWRITE_ENDPOINT:https://cloud.appwrite.io/v1}"
      },
      "description": "Appwrite backend integration"
    }
  }
}
```

## 🌐 HTTP-based MCP Servers

For remote services or custom web-based tools:

```json
{
  "mcpServers": {
    "custom_api": {
      "transport": "streamable-http",
      "url": "https://your-mcp-server.com/mcp",
      "description": "Custom HTTP MCP server"
    }
  }
}
```

## ⚙️ Advanced Configuration

### Individual Model Configuration

You can assign different AI models to different MCP tools:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "uvx",
      "args": ["mcp-server-filesystem", "/projects"],
      "model_id": "openai/gpt-4o-mini",
      "api_key": "${OPENAI_API_KEY}",
      "api_base": "https://api.openai.com/v1"
    },
    "github": {
      "command": "uvx", 
      "args": ["mcp-server-github"],
      "model_id": "anthropic/claude-3-sonnet-20240229",
      "api_key": "${ANTHROPIC_API_KEY}",
      "api_base": "https://api.anthropic.com"
    }
  }
}
```

### Environment Variables with Defaults

```json
{
  "mcpServers": {
    "example": {
      "command": "uvx",
      "args": ["mcp-server-example"],
      "env": {
        "API_KEY": "${API_KEY}",
        "TIMEOUT": "${TIMEOUT:30}",
        "DEBUG": "${DEBUG:false}"
      }
    }
  }
}
```

### Disabling Servers Temporarily

```json
{
  "mcpServers": {
    "github": {
      "_disabled": true,
      "command": "uvx",
      "args": ["mcp-server-github"]
    }
  }
}
```

## 🔧 Troubleshooting

### Check if MCP tools are loaded

```bash
# This will show all configured MCP servers and their status
xerus run --prompt "What tools are available to you?"
```

### Common Issues

**1. "MCP server not found"**
- Make sure you installed the MCP server: `uvx install mcp-server-name`
- Check that `uvx` is installed: `curl -LsSf https://astral.sh/uv/install.sh | sh`

**2. "Environment variable not found"**
- Add required variables to `~/.xerus/.env`
- Use the format: `VARIABLE_NAME=value`

**3. "Permission denied"**
- For filesystem access, make sure the path exists and is readable
- Check file permissions: `ls -la /path/to/directory`

**4. "API authentication failed"**
- Verify your API keys in `~/.xerus/.env`
- Make sure tokens have the correct permissions

### Debug MCP Configuration

You can check your MCP setup programmatically:

```python
from xerus.tools import MCPServerManager
from xerus.config import load_config

# Load and display MCP configuration
config = load_config()
mcp_manager = MCPServerManager()
mcp_manager.set_server_configs(config.get('mcpServers', {}))
mcp_manager.list_tools()
```

## 📚 Creating Custom MCP Servers

Want to create your own MCP server? Here are some resources:

- **Official MCP Documentation**: https://modelcontextprotocol.io/
- **Python MCP SDK**: https://github.com/modelcontextprotocol/python-sdk
- **TypeScript MCP SDK**: https://github.com/modelcontextprotocol/typescript-sdk

### Simple Custom HTTP MCP Server

```python
# custom_mcp_server.py
from mcp.server import Server
from mcp.server.fastapi import FastAPIServerTransport
import fastapi

app = fastapi.FastAPI()
server = Server("my-custom-server")

@server.list_tools()
async def list_tools():
    return [
        {
            "name": "get_weather",
            "description": "Get current weather for a location",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "location": {"type": "string"}
                }
            }
        }
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "get_weather":
        location = arguments.get("location")
        return f"Weather in {location}: Sunny, 72°F"

# Run with: uvicorn custom_mcp_server:app --host 0.0.0.0 --port 8000
transport = FastAPIServerTransport(app)
server.connect(transport)
```

Then configure it in Xerus:

```json
{
  "mcpServers": {
    "my_weather": {
      "transport": "streamable-http", 
      "url": "http://localhost:8000/mcp",
      "description": "Custom weather service"
    }
  }
}
```

## 🎯 Best Practices

1. **Start Simple**: Begin with one MCP tool (like filesystem) before adding more
2. **Secure Your Keys**: Always use environment variables for API keys
3. **Test Incrementally**: Add one MCP server at a time and test
4. **Use Specific Paths**: For filesystem access, use specific directories, not root (`/`)
5. **Monitor Resources**: Some MCP tools can be resource-intensive
6. **Document Your Setup**: Add descriptions to your MCP server configs

## 🚀 Next Steps

Once you have MCP tools set up:

1. **Experiment**: Try different combinations of tools for complex tasks
2. **Create Workflows**: Use MCP tools to automate your development workflow
3. **Share Configs**: Share your successful MCP configurations with your team
4. **Build Custom Tools**: Create your own MCP servers for specific needs

---

Happy building with MCP tools! 🎉 