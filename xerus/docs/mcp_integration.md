# MCP (Model Context Protocol) Integration

Xerus now supports MCP (Model Context Protocol) tools, allowing you to integrate with external services and tools using the standardized MCP protocol. This enables seamless integration with various MCP servers and their tools.

## Overview

MCP is a protocol that allows AI applications to securely connect to external services and tools. With Xerus's MCP integration, you can:

- Connect to any MCP-compatible server (both stdio-based and HTTP-based)
- Use MCP tools as first-class Xerus tools
- Maintain the same security and sandboxing as other Xerus tools
- Configure multiple MCP servers simultaneously
- Use different server types (stdio and HTTP) in the same configuration

## Server Types

Xerus supports two types of MCP servers:

### 1. Stdio-based MCP Servers
- **Description**: Run as subprocess processes communicating via stdin/stdout
- **Use Case**: Local tools and services that need direct system access
- **Security**: Higher security risk as they execute code locally
- **Configuration**: Requires `command`, `args`, and optional `env`

### 2. Streamable HTTP-based MCP Servers
- **Description**: Connect to running HTTP servers via HTTP endpoints
- **Use Case**: Remote services and web-based tools
- **Security**: Lower security risk as no local code execution
- **Configuration**: Requires `url` and `transport: "streamable-http"`

## Prerequisites

1. **Install the required packages:**
   ```bash
   # Using uv (recommended)
   uv add mcp python-dotenv
   
   # Or using pip
   pip install mcp python-dotenv
   ```

2. **For stdio-based servers - Install desired MCP server packages:**
   ```bash
   # Example: Install Appwrite MCP server
   uvx install mcp-server-appwrite
   
   # Example: Install filesystem MCP server
   uvx install mcp-server-filesystem
   
   # Example: Install GitHub MCP server
   uvx install mcp-server-github
   ```

3. **For HTTP-based servers - Ensure the server is running:**
   ```bash
   # Start your HTTP MCP server (example)
   python my_mcp_server.py --host 127.0.0.1 --port 8000
   ```

4. **Install uvx if not already installed (for stdio servers):**
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
   
   # Appwrite MCP Server (stdio)
   APPWRITE_PROJECT_ID=your_appwrite_project_id
   APPWRITE_API_KEY=your_appwrite_api_key
   APPWRITE_ENDPOINT=https://cloud.appwrite.io/v1
   
   # GitHub MCP Server (stdio)
   GITHUB_TOKEN=your_github_personal_access_token
   
   # HTTP MCP Server URLs
   HTTP_MCP_SERVER_URL=http://127.0.0.1:8000/mcp
   REMOTE_MCP_SERVER_URL=https://api.example.com/mcp
   
   # Filesystem MCP Server (stdio)
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
    "_comment": "MCP servers configuration - supports both stdio and HTTP-based servers",
    
    "stdio_appwrite": {
      "_comment": "Stdio-based MCP server example",
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
    
    "http_custom_server": {
      "_comment": "HTTP-based MCP server example",
      "transport": "streamable-http",
      "url": "${HTTP_MCP_SERVER_URL:http://127.0.0.1:8000/mcp}",
      "model_id": "openai/deepseek-ai/DeepSeek-R1-0528",
      "api_key": "${GMI_CLOUD_API_KEY}",
      "api_base": "https://api.gmi-serving.com/v1"
    },
    
    "remote_service": {
      "_comment": "Remote HTTP MCP server",
      "transport": "streamable-http",
      "url": "${REMOTE_MCP_SERVER_URL}",
      "model_id": "openai/meta-llama/Llama-4-Scout-17B-16E-Instruct",
      "api_key": "${GMI_CLOUD_API_KEY}",
      "api_base": "https://api.gmi-serving.com/v1"
    },
    
    "filesystem": {
      "_comment": "Local filesystem access via stdio",
      "command": "uvx",
      "args": ["mcp-server-filesystem", "${FILESYSTEM_ROOT_PATH:/tmp/allowed}"],
      "model_id": "openai/deepseek-ai/DeepSeek-R1-0528",
      "api_key": "${GMI_CLOUD_API_KEY}",
      "api_base": "https://api.gmi-serving.com/v1"
    },
    
    "github": {
      "_comment": "GitHub API integration via stdio",
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

#### Common Fields (both server types)
- **model_id**: (optional) Specific model to use for this MCP server's tools
- **api_key**: (optional) Specific API key for this MCP server's tools
- **api_base**: (optional) Specific API base URL for this MCP server's tools
- **_disabled**: (optional) Set to `true` to disable a server without removing its configuration

#### Stdio-based Server Fields
- **command**: The command to run the MCP server (usually `uvx`)
- **args**: Arguments to pass to the command (including the MCP server package name)
- **env**: Environment variables required by the MCP server

#### HTTP-based Server Fields
- **transport**: Must be set to `"streamable-http"` for HTTP servers
- **url**: The HTTP endpoint URL of the running MCP server

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
    },
    "http_server": {
      "_disabled": true,
      "transport": "streamable-http",
      "url": "http://127.0.0.1:8000/mcp"
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

# Use the agent with MCP tools (works with both stdio and HTTP servers)
result = manager_agent.run("List all files in the project directory")
```

### Listing Available MCP Tools

You can list all configured and loaded MCP tools:

```python
from xerus.tools import list_mcp_tools

# Show MCP configuration and loaded tools (shows server type)
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

### Stdio-based Servers

#### Appwrite
**Package**: `mcp-server-appwrite`
**Description**: Integrate with Appwrite backend services
**Environment Variables**:
- `APPWRITE_PROJECT_ID`: Your Appwrite project ID
- `APPWRITE_API_KEY`: Your Appwrite API key
- `APPWRITE_ENDPOINT`: Appwrite endpoint (optional, defaults to cloud)

#### Filesystem
**Package**: `mcp-server-filesystem`
**Description**: Safe filesystem access within specified directories
**Arguments**: Path to the allowed directory
**Security**: Only allows access to the specified directory and subdirectories

#### GitHub
**Package**: `mcp-server-github`
**Description**: GitHub API integration for repository management
**Environment Variables**:
- `GITHUB_PERSONAL_ACCESS_TOKEN`: Your GitHub personal access token

#### SQLite
**Package**: `mcp-server-sqlite`
**Description**: SQLite database tools and queries
**Arguments**: Path to the SQLite database file

### HTTP-based Servers

HTTP-based MCP servers are typically custom implementations or services that expose MCP functionality over HTTP. These need to be running independently before connecting to them.

## Security Considerations

### General Security
1. **Trust Remote Code**: MCP tools are loaded with `trust_remote_code=True` by default. Only use MCP servers from trusted sources.

2. **Environment Variables**: Store sensitive information (API keys, tokens) in environment variables, not directly in the config file.

3. **Sandboxing**: MCP tools run in the same sandbox as other Xerus tools, providing isolation and security.

### Stdio-based Server Security
- **Higher Risk**: Stdio servers execute code on your local machine
- **System Access**: Can access local files, network, and system resources
- **Recommendation**: Only use well-known, trusted MCP server packages

### HTTP-based Server Security
- **Lower Risk**: No local code execution
- **Network Only**: Communication happens over HTTP/HTTPS
- **Considerations**: 
  - Ensure HTTPS for production use
  - Verify server certificates
  - Use authentication if available
  - Monitor network traffic if needed

## Troubleshooting

### Common Issues

1. **MCP Package Not Found**
   ```
   Error: mcp package not found
   ```
   **Solution**: Install the MCP package: `uv add mcp` or `pip install mcp`

2. **Stdio Server Not Found**
   ```
   Error loading tools from MCP server 'servername'
   Make sure the MCP server package is installed and configured correctly
   ```
   **Solution**: Install the MCP server package: `uvx install mcp-server-name`

3. **HTTP Server Connection Failed**
   ```
   Error loading tools from MCP server 'servername'
   Make sure the HTTP MCP server is running and accessible at the configured URL
   ```
   **Solution**: 
   - Verify the HTTP server is running
   - Check the URL is correct and accessible
   - Ensure network connectivity

4. **Environment Variables Not Set**
   ```
   Error: Missing required environment variable
   ```
   **Solution**: Set the required environment variables or add them to the `env` section in config

5. **Permission Denied**
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

### Server Type Detection

The system automatically detects server type based on configuration:
- If `transport: "streamable-http"` is present → HTTP-based server
- Otherwise → stdio-based server

Check the console output when loading to see which type is detected:
```
[blue]Connecting to HTTP-based MCP server: my_server[/blue]
[blue]Connecting to stdio-based MCP server: my_other_server[/blue]
```

## Examples

See `xerus/examples/mcp_example.py` for a complete example of using both stdio and HTTP-based MCP tools with Xerus.

## Contributing

To add support for new MCP servers:

1. For stdio servers: Install the MCP server package
2. For HTTP servers: Set up the HTTP server independently
3. Add configuration to your `config.json`
4. Test the integration
5. Submit documentation updates if the server works well with Xerus

For issues or feature requests related to MCP integration, please open an issue on the Xerus repository.