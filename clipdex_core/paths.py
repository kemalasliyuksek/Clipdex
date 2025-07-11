from pathlib import Path
import os
import sys

def get_user_data_dir() -> Path:
    """Creates/returns a writable folder in the user's data directory based on platform."""
    if sys.platform.startswith("win"):
        # Windows: %LOCALAPPDATA%
        base_dir = Path(os.getenv("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
    elif sys.platform == "darwin":
        # macOS: ~/Library/Application Support
        base_dir = Path.home() / "Library" / "Application Support"
    else:
        # Linux and other Unix-like systems: ~/.local/share
        base_dir = Path.home() / ".local" / "share"
    
    data_dir = base_dir / "Clipdex"
    try:
        data_dir.mkdir(parents=True, exist_ok=True)
    except PermissionError:
        # Very rare, but if there are permission issues, fall back to home directory
        fallback = Path.home() / ".clipdex"
        fallback.mkdir(parents=True, exist_ok=True)
        return fallback
    return data_dir 