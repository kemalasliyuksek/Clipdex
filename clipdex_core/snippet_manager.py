import json
import os
from pathlib import Path
import sys
import shutil
from typing import Union

from .paths import get_user_data_dir

class SnippetManager:
    """
    Manages shortcut data (snippets) through a JSON file.
    Reads, writes, and ensures the file exists.
    """
    def __init__(self, filepath: Union[str, Path, None] = None):
        """Creates a new SnippetManager.

        If *filepath* is not provided, the file path is automatically set to the user's LOCALAPPDATA folder.
        """
        if filepath is None:
            filepath = get_user_data_dir() / "snippets.json"

        # No need to convert Path object to string; os and open accept it.
        self.filepath: Union[Path, str] = filepath
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """Ensures that the JSON file exists. If not, try to copy a bundled default; otherwise create empty."""
        if os.path.exists(self.filepath):
            return

        # 1) Check if there's a bundled default file
        try:
            # Under PyInstaller, sys._MEIPASS is a temporary folder; during development, we use the module root.
            base_path = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent.parent.parent))
            default_path = base_path / "snippets.json"
            if default_path.exists():
                shutil.copy(default_path, self.filepath)
                return
        except Exception:
            # If copying fails, continue silently
            pass

        # 2) If no default file exists, create an empty file
        self.save_snippets({})

    def load_snippets(self):
        """Loads shortcuts from the JSON file and returns them as a dictionary."""
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # Return an empty dictionary if the file is not found or is corrupted.
            return {}

    def save_snippets(self, snippets_data: dict):
        """Saves the given dictionary to the JSON file."""
        with open(self.filepath, 'w', encoding='utf-8') as f:
            # indent=4: Makes the file more readable.
            # ensure_ascii=False: Properly saves Turkish characters.
            json.dump(snippets_data, f, indent=4, ensure_ascii=False)