import json
import os

class SnippetManager:
    """
    Manages shortcut data (snippets) through a JSON file.
    Reads, writes, and ensures the file exists.
    """
    def __init__(self, filepath='snippets.json'):
        self.filepath = filepath
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """Ensures that the JSON file exists. If not, it creates an empty file."""
        if not os.path.exists(self.filepath):
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