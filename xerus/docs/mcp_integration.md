# MCP (Model Context Protocol) Integration

Xerus now supports MCP (Model Context Protocol) tools, allowing you to integrate with external services and tools using the standardized MCP protocol. This enables seamless integration with various MCP servers and their tools.

## Overview

MCP is a protocol that allows AI applications to securely connect to external services and tools. With Xerus's MCP integration, you can:

- Connect to any MCP-compatible server
- Use MCP tools as first-class Xerus tools
- Maintain the same security and sandboxing as other Xerus tools
- Configure multiple MCP servers simultaneously

## Prerequisites

1. **Install the required packages:**
   ```bash
   # Using uv (recommended)
   uv add mcp python-dotenv
   
   # Or using pip
   pip install mcp python-dotenv
   ```

2. **Install desired MCP server packages:**
   ```bash
   # Example: Install Appwrite MCP server
   uvx install mcp-server-appwrite
   
   # Example: Install filesystem MCP server
   uvx install mcp-server-filesystem
   
   # Example: Install GitHub MCP server
   uvx install mcp-server-github
   ```

3. **Install uvx if not already installed:**
   ```bash
   # Using uv
   uv tool install uvx
   
   # Or using pip
   pip install uvx
   ```

## Configuration

### Environment Variables

Xerus supports loading environment variables from a `.env` file and using variable substitution in the configuration:

1. **Create a `.env` file** at `~/.xerus/.env`:
   ```bash
   # API Configuration
   GMI_CLOUD_API_KEY=your_gmi_cloud_api_key
   
   # Appwrite MCP Server
   APPWRITE_PROJECT_ID=your_appwrite_project_id
   APPWRITE_API_KEY=your_appwrite_api_key
   APPWRITE_ENDPOINT=https://cloud.appwrite.io/v1
   
   # GitHub MCP Server
   GITHUB_TOKEN=your_github_personal_access_token
   
   # Filesystem MCP Server
   FILESYSTEM_ROOT_PATH=/path/to/allowed/directory
   ```

2. **Use variable substitution** in your config.json:
   - `${VAR_NAME}` - Required variable (will use empty string if not found)
   - `${VAR_NAME:default_value}` - Variable with default value

### Adding MCP Servers to Config

Add MCP servers to your `~/.xerus/config.json` file using the `mcpServers` section. Each server can have its own model configuration:

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
      "model_id": "openai/meta-llama/Llama-4-Scout-17B-16E-Instruct",
      "api_key": "${GMI_CLOUD_API_KEY}",
      "api_base": "https://api.gmi-serving.com/v1"
    },
    "filesystem": {
      "command": "uvx",
      "args": ["mcp-server-filesystem", "${FILESYSTEM_ROOT_PATH:/tmp/allowed}"],
      "model_id": "openai/deepseek-ai/DeepSeek-R1-0528",
      "api_key": "${GMI_CLOUD_API_KEY}",
      "api_base": "https://api.gmi-serving.com/v1"
    },
    "github": {
      "command": "uvx",
      "args": ["mcp-server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
      },
      "model_id": "openai/meta-llama/Llama-4-Scout-17B-16E-Instruct",
      "api_key": "${GMI_CLOUD_API_KEY}",
      "api_base": "https://api.gmi-serving.com/v1"
    }
  }
}
```

### Configuration Fields

- **command**: The command to run the MCP server (usually `uvx`)
- **args**: Arguments to pass to the command (including the MCP server package name)
- **env**: Environment variables required by the MCP server
- **model_id**: (optional) Specific model to use for this MCP server's tools
- **api_key**: (optional) Specific API key for this MCP server's tools
- **api_base**: (optional) Specific API base URL for this MCP server's tools
- **_disabled**: (optional) Set to `true` to disable a server without removing its configuration

**Note**: If model configuration is not specified for an MCP server, it will use the manager agent's model configuration as the default.

### Disabling Servers

To temporarily disable an MCP server without removing its configuration:

```json
{
  "mcpServers": {
    "appwrite": {
      "_disabled": true,
      "command": "uvx",
      "args": ["mcp-server-appwrite"],
      "env": {
        "APPWRITE_PROJECT_ID": "your-project-id",
        "APPWRITE_API_KEY": "your-api-key"
      }
    }
  }
}
```

## Usage

### Using MCP Tools with Xerus

Once configured, MCP tools are automatically loaded and available through your Xerus manager agent:

```python
from xerus.tools import setup_manager_agent

# Create manager agent with all tools (including MCP tools)
manager_agent = setup_manager_agent()

# Use the agent with MCP tools
result = manager_agent.run("List all files in the project directory")
```

### Listing Available MCP Tools

You can list all configured and loaded MCP tools:

```python
from xerus.tools import list_mcp_tools

# Show MCP configuration and loaded tools
list_mcp_tools()
```

### Programmatic Access

You can also load MCP tools programmatically:

```python
from xerus.tools import load_mcp_tools
from xerus.config import load_config

config = load_config()
mcp_servers = config.get('mcpServers', {})
mcp_tools = load_mcp_tools(mcp_servers)

print(f"Loaded {len(mcp_tools)} MCP tools")
for tool in mcp_tools:
    print(f"- {tool.name}: {tool.description}")
```

## Popular MCP Servers

### Appwrite
**Package**: `mcp-server-appwrite`
**Description**: Integrate with Appwrite backend services
**Environment Variables**:
- `APPWRITE_PROJECT_ID`: Your Appwrite project ID
- `APPWRITE_API_KEY`: Your Appwrite API key
- `APPWRITE_ENDPOINT`: Appwrite endpoint (optional, defaults to cloud)

### Filesystem
**Package**: `mcp-server-filesystem`
**Description**: Safe filesystem access within specified directories
**Arguments**: Path to the allowed directory
**Security**: Only allows access to the specified directory and subdirectories

### GitHub
**Package**: `mcp-server-github`
**Description**: GitHub API integration for repository management
**Environment Variables**:
- `GITHUB_PERSONAL_ACCESS_TOKEN`: Your GitHub personal access token

### SQLite
**Package**: `mcp-server-sqlite`
**Description**: SQLite database tools and queries
**Arguments**: Path to the SQLite database file

## Security Considerations

1. **Trust Remote Code**: MCP tools are loaded with `trust_remote_code=True` by default. Only use MCP servers from trusted sources.

2. **Environment Variables**: Store sensitive information (API keys, tokens) in environment variables, not directly in the config file.

3. **Sandboxing**: MCP tools run in the same sandbox as other Xerus tools, providing isolation and security.

4. **Network Access**: Some MCP servers may require network access to external services.

## Troubleshooting

### Common Issues

1. **MCP Package Not Found**
   ```
   Error: mcp package not found
   ```
   **Solution**: Install the MCP package: `uv add mcp` or `pip install mcp`

2. **MCP Server Not Found**
   ```
   Error loading tools from MCP server 'servername'
   ```
   **Solution**: Install the MCP server package: `uvx install mcp-server-name`

3. **Environment Variables Not Set**
   ```
   Error: Missing required environment variable
   ```
   **Solution**: Set the required environment variables or add them to the `env` section in config

4. **Permission Denied**
   ```
   Error: Permission denied when accessing MCP server
   ```
   **Solution**: Check that the MCP server has the necessary permissions and credentials

### Debug Mode

Enable verbose logging to see detailed MCP loading information:

```python
from xerus.tools import setup_manager_agent

# Create agent with verbose logging
manager_agent = setup_manager_agent(verbosity_level=3)
```

## Examples

See `xerus/examples/mcp_example.py` for a complete example of using MCP tools with Xerus.

## Contributing

To add support for new MCP servers:

1. Install the MCP server package
2. Add configuration to your `config.json`
3. Test the integration
4. Submit documentation updates if the server works well with Xerus

For issues or feature requests related to MCP integration, please open an issue on the Xerus repository.