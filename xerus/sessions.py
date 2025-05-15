"""
Session management utilities for Xerus CLI.
"""
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

def get_history_file_path() -> Path:
    """Get the path to the conversation history file."""
    xerus_dir = Path.home() / ".xerus"
    xerus_dir.mkdir(exist_ok=True)
    return xerus_dir / "history.json"

def get_session_dir() -> Path:
    """Get the directory for session data."""
    xerus_dir = Path.home() / ".xerus" / "sessions"
    xerus_dir.mkdir(exist_ok=True, parents=True)
    return xerus_dir

def create_session_file(name=None) -> Path:
    """Create a new session file with optional name."""
    session_dir = get_session_dir()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    name_part = f"_{name}" if name else ""
    session_file = session_dir / f"session{name_part}_{timestamp}.json"
    return session_file

def load_conversation_history() -> List[Dict[str, Any]]:
    """Load conversation history from file."""
    history_file = get_history_file_path()
    if history_file.exists():
        try:
            with open(history_file, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            from .ui.display import console
            console.print("[yellow]Warning: Could not parse history file. Starting with empty history.[/yellow]")
    return []

def save_conversation_history(history: List[Dict[str, Any]]):
    """Save conversation history to file."""
    history_file = get_history_file_path()
    # Limit history to last 50 exchanges to prevent file from growing too large
    history_to_save = history[-50:] if len(history) > 50 else history
    with open(history_file, "w") as f:
        json.dump(history_to_save, f)

def save_session(session_file: Path, history: List[Dict[str, Any]], metadata: Dict[str, Any] = None):
    """Save session to a file."""
    data = {
        "history": history,
        "timestamp": datetime.now().isoformat(),
        "metadata": metadata or {}
    }
    with open(session_file, "w") as f:
        json.dump(data, f, indent=2)
    return session_file

def load_session(session_file: Path) -> Dict[str, Any]:
    """Load a session from a file."""
    with open(session_file, "r") as f:
        return json.load(f)
