from pathlib import Path
import os

def get_user_data_dir() -> Path:
    """Creates/returns a writable folder in the user's LOCALAPPDATA on Windows."""
    # %LOCALAPPDATA% is usually present, but we provide a backup just in case
    base_dir = Path(os.getenv("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
    data_dir = base_dir / "Clipdex"
    try:
        data_dir.mkdir(parents=True, exist_ok=True)
    except PermissionError:
        # Very rare, but if there are permission issues, fall back to home directory
        fallback = Path.home() / ".clipdex"
        fallback.mkdir(parents=True, exist_ok=True)
        return fallback
    return data_dir 