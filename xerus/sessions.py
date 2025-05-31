"""
Session management utilities for Xerus CLI.
"""
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

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
