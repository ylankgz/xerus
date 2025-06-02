# 🔒 Security & Import Configuration Guide

This guide covers the security aspects of Xerus's CodeAct agents, focusing on Python library import configuration and best practices for safe usage across different environments.

## 📋 Table of Contents

- [Overview](#overview)
- [Runtime Environment](#runtime-environment)
- [Import Configuration](#import-configuration)
- [Security Modes](#security-modes)
- [Configuration Examples](#configuration-examples)
- [Best Practices](#best-practices)
- [Environment-Specific Guidelines](#environment-specific-guidelines)
- [Advanced Sandboxing Options](#advanced-sandboxing-options)
- [Troubleshooting](#troubleshooting)

## 🏗️ Overview

**⚠️ Critical Security Information**: Xerus CodeAct agents execute Python code directly on your machine using your local Python runtime. Unlike sandboxed environments, this provides full access to your system resources, making proper configuration essential.

> 📖 **Additional Reading**: For more details about the underlying security mechanisms, see the [smolagents Secure Code Execution documentation](https://huggingface.co/docs/smolagents/tutorials/secure_code_execution), which explains the custom Python interpreter and sandboxing options that Xerus builds upon.

### What This Means

- **Direct System Access**: Code runs with your user permissions
- **File System Access**: Can read, write, and delete files you have access to
- **Network Access**: Can make HTTP requests, download files, connect to databases
- **Package Installation**: Can install Python packages if you have permissions
- **System Commands**: Can execute shell commands (when unrestricted)

## 🏗️ Runtime Environment

### System Integration

Xerus CodeAct agents execute code using:

| Component | Details |
|-----------|---------|
| **Operating System** | Your local OS (Linux, macOS, Windows) |
| **Python Runtime** | Your installed Python version and environment |
| **File Permissions** | Your user account's file system permissions |
| **Network Access** | Your machine's network connection and firewall rules |
| **Environment Variables** | Access to your shell environment variables |
| **Installed Packages** | All Python packages in your current environment |

### Security Implications

- **Local Development**: High risk - can access personal files, credentials, private projects
- **Remote Servers**: Medium risk - isolated environment, limited personal data exposure
- **Docker Containers**: Low risk - containerized and isolated from host system
- **Production Systems**: **Never recommended** - potential for system disruption

## 📚 Import Configuration

The `authorized_imports` parameter in `~/.xerus/config.json` controls which Python libraries the CodeAct agent can import and use.

### Configuration Location

```json
{
  "tools": {
    "python_interpreter_agent": {
      "code_agent": true,
      "name": "python_interpreter_agent",
      "description": "Executes Python code",
      "tool_class": "smolagents.PythonInterpreterTool",
      "model_id": "your-model-id",
      "api_key": "${YOUR_API_KEY}",
      "api_base": "your-api-base",
      "parameters": {
        "authorized_imports": ["math", "random", "datetime", "json", "re"]
      }
    }
  }
}
```

## 🛡️ Security Modes

### 🔐 Restricted Mode (Recommended for Local Development)

**Configuration:**
```json
"authorized_imports": ["math", "random", "datetime", "json", "re"]
```

**Characteristics:**
- ✅ Limits to specific, pre-approved libraries
- ✅ Prevents dangerous system operations
- ✅ Safe for personal development machines
- ✅ Reduces risk of unintended system modifications
- ❌ May limit functionality for complex tasks

### ⚠️ Full Access Mode (Caution Required)

**Configuration:**
```json
"authorized_imports": ["*"]
```

**Characteristics:**
- ✅ Maximum functionality and flexibility
- ✅ Can perform any Python operation
- ✅ Suitable for isolated environments
- ❌ **High security risk on local machines**
- ❌ Can access sensitive files and system resources
- ❌ Potential for unintended system modifications

## 🎯 Configuration Examples

### 📊 Data Science Configuration

Perfect for data analysis, visualization, and basic machine learning:

```json
"authorized_imports": [
  "math", "random", "datetime", "json", "re",
  "pandas", "numpy", "matplotlib", "seaborn", 
  "plotly", "scipy", "statsmodels"
]
```

**Use Cases:**
- Data cleaning and transformation
- Statistical analysis
- Data visualization
- Basic exploratory data analysis

### 🤖 Machine Learning Configuration

For comprehensive ML workflows including deep learning:

```json
"authorized_imports": [
  "math", "random", "datetime", "json", "re",
  "pandas", "numpy", "matplotlib", "seaborn",
  "sklearn", "scipy", "joblib",
  "torch", "tensorflow", "keras",
  "transformers", "datasets", "tokenizers",
  "optuna", "mlflow"
]
```

**Use Cases:**
- Model training and evaluation
- Hyperparameter optimization
- Neural network development
- MLOps workflows

### 🌐 Web Development & APIs

For web scraping, API development, and HTTP operations:

```json
"authorized_imports": [
  "math", "random", "datetime", "json", "re",
  "requests", "urllib", "http", "json",
  "beautifulsoup4", "lxml", "selenium",
  "fastapi", "flask", "django"
]
```

**Use Cases:**
- Web scraping and data collection
- API development and testing
- HTTP client operations
- Simple web applications

### 🔬 Scientific Computing

For advanced scientific computations and research:

```json
"authorized_imports": [
  "math", "random", "datetime", "json", "re",
  "numpy", "scipy", "sympy", "matplotlib",
  "pandas", "statsmodels", "scikit-image",
  "opencv-python", "pillow", "networkx",
  "biopython", "astropy"
]
```

**Use Cases:**
- Scientific research and computation
- Image and signal processing
- Mathematical modeling
- Specialized domain analysis

### 🚀 Full Development Environment (Remote/Docker Only)

**⚠️ WARNING: Use only in isolated environments**

```json
"authorized_imports": ["*"]
```

**Use Cases:**
- Complete development workflows
- System administration tasks
- Package management and installation
- File system operations
- Database administration

## 🛡️ Best Practices

### 🔐 Security Guidelines

1. **Start Restrictive**: Begin with minimal imports and add as needed
2. **Environment Awareness**: Use different configurations for different environments
3. **Regular Audits**: Periodically review your authorized imports
4. **Principle of Least Privilege**: Only allow what's necessary for your tasks
5. **Monitor Activity**: Keep track of what code is being executed

### 📋 Configuration Management

1. **Version Control**: Track changes to your configuration
2. **Environment-Specific Configs**: Use different configs for dev/staging/prod
3. **Documentation**: Document why specific libraries are authorized
4. **Regular Updates**: Keep your authorized list current with your needs

### 🔄 Workflow Recommendations

1. **Development Cycle**:
   ```
   Start Restricted → Test Functionality → Add Required Libraries → Validate Security → Deploy
   ```

2. **Library Addition Process**:
   - Identify the specific library needed
   - Research the library's security implications
   - Add to authorized imports
   - Test functionality
   - Document the addition

## 🌍 Environment-Specific Guidelines

### 💻 Local Development Machine

**Recommended Approach**: **Restricted Mode**

```json
"authorized_imports": [
  "math", "random", "datetime", "json", "re",
  "pandas", "numpy", "matplotlib", "sklearn"
]
```

**Rationale**:
- Protects personal files and credentials
- Prevents accidental system modifications
- Limits exposure of sensitive development data
- Still provides substantial functionality

### 🖥️ Remote Development Server

**Recommended Approach**: **Controlled Full Access** or **Extended Restricted**

```json
"authorized_imports": ["*"]
```

**Or for more control**:
```json
"authorized_imports": [
  "math", "random", "datetime", "json", "re",
  "pandas", "numpy", "matplotlib", "seaborn", "plotly",
  "sklearn", "scipy", "torch", "tensorflow",
  "requests", "beautifulsoup4", "selenium",
  "fastapi", "flask", "sqlalchemy", "psycopg2",
  "boto3", "paramiko", "fabric"
]
```

**Rationale**:
- Isolated from personal data
- Designed for development workflows
- Can afford more permissive access
- Still maintains some operational security

### 🐳 Docker Container

**Recommended Approach**: **Full Access**

```json
"authorized_imports": ["*"]
```

**Rationale**:
- Completely isolated from host system
- Container can be easily rebuilt if compromised
- Maximum functionality without security concerns
- Perfect for experimentation and development

### 🏭 Production Environment

**Recommended Approach**: **Highly Restricted or Not Recommended**

```json
"authorized_imports": [
  "math", "datetime", "json", "re"
]
```

**Rationale**:
- Production systems require maximum stability
- Minimize attack surface
- Prevent unintended system modifications
- Consider using pre-built, tested solutions instead


## 🚫 Security Warnings

### 🚫 Never Do This

1. **Local Machine with Full Access**:
   ```json
   "authorized_imports": ["*"]  // ❌ DANGEROUS on local machines
   ```

2. **Production Systems**:
   ```json
   // ❌ Don't use Xerus agents in production
   ```

3. **Shared Systems**:
   ```json
   // ❌ Avoid on multi-user systems without isolation
   ```

### ⚠️ High-Risk Libraries

Be especially cautious with these library categories:

- **System Operations**: `os`, `sys`, `subprocess`, `shutil`
- **Network Operations**: `socket`, `urllib`, `requests` (in unrestricted mode)
- **File Operations**: `pathlib`, `glob`, `tempfile`
- **Process Management**: `multiprocessing`, `threading`
- **Database Connections**: `sqlite3`, `psycopg2`, `pymongo`

## 🔧 Troubleshooting

### Common Import Errors

**Error**: `ImportError: Module 'pandas' not allowed`
**Solution**: Add `"pandas"` to your `authorized_imports` list

**Error**: `ImportError: Wildcard imports not allowed`
**Solution**: Either specify individual modules or use `"*"` for full access

### Configuration Issues

**Problem**: Changes not taking effect
**Solution**: Restart your Xerus session after modifying config.json

**Problem**: Library available in Python but blocked by Xerus
**Solution**: Ensure the exact module name is in your `authorized_imports` list

### Security Concerns

**Problem**: Worried about security but need more functionality
**Solution**: Use Docker or remote server with full access, or carefully curate your library list

**Problem**: Code trying to access unauthorized resources
**Solution**: Review and expand your `authorized_imports` or investigate why the code needs those resources

## 🔄 Applying Configuration Changes

After modifying your `~/.xerus/config.json`, you need to restart your Xerus session:

1. **Exit current session**: Use `Ctrl+C` or `exit` command
2. **Start new session**: Run `xerus chat` or `xerus run`
3. **Verify changes**: Test that new imports work or restrictions are applied

## 📞 Getting Help

If you encounter security concerns or configuration issues:

1. **Check this documentation** for common scenarios
2. **Review the [Config Customization Guide](CONFIG_CUSTOMIZATION.md)** for advanced options
3. **Open an issue** on [GitHub](https://github.com/ylankgz/xerus/issues)
4. **Join discussions** on [GitHub Discussions](https://github.com/ylankgz/xerus/discussions)

---

**Remember**: Security is a balance between functionality and risk. Choose the configuration that best fits your environment and use case while maintaining appropriate security standards. 