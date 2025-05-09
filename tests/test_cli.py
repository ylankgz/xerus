"""
Tests for the CLI module.
"""
import os
import pytest
from unittest.mock import patch, MagicMock
from click.testing import CliRunner

from xerus.cli import cli, create_agent, get_model

@pytest.fixture
def runner():
    """Create a CLI runner for testing."""
    return CliRunner()

def test_cli_help(runner):
    """Test that the CLI help command works."""
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "Xerus - CLI Agent powered by Huggingface Smolagents" in result.output

def test_run_help(runner):
    """Test that the run command help works."""
    result = runner.invoke(cli, ["run", "--help"])
    assert result.exit_code == 0
    assert "Run the agent with a prompt" in result.output

@patch("xerus.cli.CodeAgent")
@patch("xerus.cli.get_model")
def test_create_agent(mock_get_model, mock_code_agent):
    """Test the create_agent function."""
    mock_model = MagicMock()
    mock_get_model.return_value = mock_model
    mock_agent = MagicMock()
    mock_code_agent.return_value = mock_agent
    
    agent = create_agent("inference", "model-id", tools=["web_search"], imports="pandas numpy")
    
    mock_get_model.assert_called_once_with("inference", "model-id", None)
    assert mock_code_agent.call_count == 1
    # Check that WebSearchTool was included
    assert len(mock_code_agent.call_args[1]["tools"]) == 1
    # Check that imports were included
    assert "pandas" in mock_code_agent.call_args[1]["additional_authorized_imports"]
    assert "numpy" in mock_code_agent.call_args[1]["additional_authorized_imports"]
    assert agent == mock_agent

@patch("xerus.cli.InferenceClientModel")
def test_get_model_inference(mock_inference_model):
    """Test get_model with inference type."""
    mock_model = MagicMock()
    mock_inference_model.return_value = mock_model
    
    model = get_model("inference", "model-id")
    
    mock_inference_model.assert_called_once_with(model_id="model-id")
    assert model == mock_model

@patch("xerus.cli.OpenAIServerModel")
def test_get_model_openai(mock_openai_model):
    """Test get_model with openai type."""
    mock_model = MagicMock()
    mock_openai_model.return_value = mock_model
    
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
        model = get_model("openai", "model-id")
    
    mock_openai_model.assert_called_once_with(model_id="model-id", api_key="test-key")
    assert model == mock_model

@patch("xerus.cli.LiteLLMModel")
def test_get_model_litellm(mock_litellm_model):
    """Test get_model with litellm type."""
    mock_model = MagicMock()
    mock_litellm_model.return_value = mock_model
    
    model = get_model("litellm", "model-id", api_key="custom-key")
    
    mock_litellm_model.assert_called_once_with(model_id="model-id", api_key="custom-key")
    assert model == mock_model

@patch("xerus.cli.TransformersModel")
def test_get_model_transformers(mock_transformers_model):
    """Test get_model with transformers type."""
    mock_model = MagicMock()
    mock_transformers_model.return_value = mock_model
    
    model = get_model("transformers", "model-id")
    
    mock_transformers_model.assert_called_once()
    assert model == mock_model

def test_get_model_unknown():
    """Test get_model with unknown type."""
    with pytest.raises(ValueError, match="Unknown model type: unknown"):
        get_model("unknown", "model-id") 